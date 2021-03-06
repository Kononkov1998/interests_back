import tmdbsimple as tmdb
from django.core.cache import cache
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from requests import HTTPError
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from movies.models import Movie, UserMovie, Genre, MovieGenre
from movies.serializers import UserMovieSerializer, FollowedUserMovieSerializer
from users.models import UserFollow
from utils.constants import LANGUAGE, ERROR, MOVIE_NOT_FOUND, TMDB_UNAVAILABLE, CACHE_TIMEOUT
from utils.documentation import MOVIES_SEARCH_200_EXAMPLE, MOVIE_RETRIEVE_200_EXAMPLE
from utils.functions import update_fields_if_needed, get_tmdb_movie_key
from utils.openapi_params import query_param, page_param, DEFAULT_PAGE_NUMBER


class SearchMoviesViewSet(GenericViewSet, mixins.ListModelMixin):
    @swagger_auto_schema(manual_parameters=[query_param, page_param],
                         responses={
                             status.HTTP_200_OK: openapi.Response(
                                 description=status.HTTP_200_OK,
                                 examples={
                                     "application/json": MOVIES_SEARCH_200_EXAMPLE
                                 }

                             )
                         })
    def list(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        page = request.GET.get('page', DEFAULT_PAGE_NUMBER)
        try:
            results = get_movie_search_results(query=query, page=page)
        except HTTPError:
            results = None
        return Response(results, status=status.HTTP_200_OK)


class MovieViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    queryset = UserMovie.objects.all()
    serializer_class = UserMovieSerializer
    lookup_field = 'tmdb_id'

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: openapi.Response(
            description=status.HTTP_200_OK,
            examples={
                "application/json": MOVIE_RETRIEVE_200_EXAMPLE
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description=status.HTTP_404_NOT_FOUND,
            examples={
                "application/json": {
                    ERROR: MOVIE_NOT_FOUND
                }
            }
        ),
        status.HTTP_503_SERVICE_UNAVAILABLE: openapi.Response(
            description=status.HTTP_503_SERVICE_UNAVAILABLE,
            examples={
                "application/json": {
                    ERROR: TMDB_UNAVAILABLE
                },
            }
        )
    })
    def retrieve(self, request, *args, **kwargs):
        try:
            tmdb_movie, returned_from_cache = get_tmdb_movie(kwargs.get('tmdb_id'))
            tmdb_cast_crew = get_cast_crew(kwargs.get('tmdb_id'))
            tmdb_movie['cast'] = tmdb_cast_crew.get('cast')
            tmdb_movie['crew'] = tmdb_cast_crew.get('crew')
        except HTTPError as e:
            error_code = int(e.args[0].split(' ', 1)[0])
            if error_code == 404:
                return Response({ERROR: MOVIE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
            return Response({ERROR: TMDB_UNAVAILABLE}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except ConnectionError:
            return Response({ERROR: TMDB_UNAVAILABLE}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        new_fields = {
            'imdb_id': tmdb_movie.get('imdb_id'),
            'tmdb_original_name': tmdb_movie.get('original_title'),
            'tmdb_name': tmdb_movie.get('title'),
            'tmdb_runtime': tmdb_movie.get('runtime'),
            'tmdb_release_date': tmdb_movie.get('release_date') if tmdb_movie.get('release_date') != "" else None
        }

        with transaction.atomic():
            movie, created = Movie.objects.select_for_update().get_or_create(tmdb_id=tmdb_movie.get('id'),
                                                                             defaults=new_fields)
            if not created and not returned_from_cache:
                update_fields_if_needed(movie, new_fields)

        if created or not returned_from_cache:
            for genre in tmdb_movie.get('genres'):
                genre_obj, created = Genre.objects.get_or_create(tmdb_id=genre.get('id'),
                                                                 defaults={
                                                                     'tmdb_name': genre.get('name')
                                                                 })
                MovieGenre.objects.get_or_create(genre=genre_obj, movie=movie)

        return Response({'tmdb': tmdb_movie})

    @swagger_auto_schema(responses={status.HTTP_200_OK: FollowedUserMovieSerializer(many=True)})
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def user_info(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(tmdb_id=kwargs.get('tmdb_id'))

            try:
                user_movie = UserMovie.objects.exclude(status=UserMovie.STATUS_NOT_WATCHED).get(user=request.user,
                                                                                                movie=movie)
                user_info = self.get_serializer(user_movie).data
            except UserMovie.DoesNotExist:
                user_info = None

            user_follow_query = UserFollow.objects.filter(user=request.user).values('followed_user')
            followed_user_movies = UserMovie.objects.filter(user__in=user_follow_query, movie=movie)
            serializer = FollowedUserMovieSerializer(followed_user_movies, many=True)
            friends_info = serializer.data
        except (Movie.DoesNotExist, ValueError):
            user_info = None
            friends_info = ()

        return Response({'user_info': user_info, 'friends_info': friends_info})

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=list(dict(UserMovie.STATUS_CHOICES).keys()) + list(dict(UserMovie.STATUS_CHOICES).values())
            ),
            "score": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                minimum=UserMovie._meta.get_field('score').validators[0].limit_value,
                maximum=UserMovie._meta.get_field('score').validators[1].limit_value
            ),
            "review": openapi.Schema(
                type=openapi.TYPE_STRING,
                maxLength=UserMovie._meta.get_field('review').max_length
            )
        }
    ),
        responses={
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description=status.HTTP_404_NOT_FOUND,
                examples={
                    "application/json": {
                        ERROR: MOVIE_NOT_FOUND
                    }
                }
            ),
            status.HTTP_503_SERVICE_UNAVAILABLE: openapi.Response(
                description=status.HTTP_503_SERVICE_UNAVAILABLE,
                examples={
                    "application/json": {
                        ERROR: TMDB_UNAVAILABLE
                    },
                }
            )
        }
    )
    def update(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(tmdb_id=kwargs.get('tmdb_id'))
        except Movie.DoesNotExist:
            return Response({ERROR: MOVIE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data.update({'user': request.user.pk,
                     'movie': movie.pk})

        try:
            user_movie = UserMovie.objects.get(user=request.user, movie=movie)
            serializer = self.get_serializer(user_movie, data=data)
        except UserMovie.DoesNotExist:
            serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


def get_movie_search_results(query, page):
    key = f'tmdb_movie_search_{query}_page_{page}'
    results = cache.get(key, None)
    if results is None:
        results = tmdb.Search().movie(query=query, page=page, language=LANGUAGE)
        cache.set(key, results, CACHE_TIMEOUT)
    return results


def get_tmdb_movie(tmdb_id):
    returned_from_cache = True
    key = get_tmdb_movie_key(tmdb_id)
    tmdb_movie = cache.get(key, None)
    if tmdb_movie is None:
        tmdb_movie = tmdb.Movies(tmdb_id).info(language=LANGUAGE)
        cache.set(key, tmdb_movie, CACHE_TIMEOUT)
        returned_from_cache = False
    return tmdb_movie, returned_from_cache


def get_cast_crew(tmdb_id):
    key = f'movie_{tmdb_id}_cast_crew'
    tmdb_cast_crew = cache.get(key, None)
    if tmdb_cast_crew is None:
        tmdb_cast_crew = tmdb.Movies(tmdb_id).credits(language=LANGUAGE)
        cache.set(key, tmdb_cast_crew, CACHE_TIMEOUT)
    return tmdb_cast_crew

# Generated by Django 3.1.6 on 2021-02-12 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20210212_1606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='receive_episodes_release_email',
            new_name='receive_episodes_releases',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='receive_game_release_email',
            new_name='receive_games_releases',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='receive_movie_release_email',
            new_name='receive_movies_releases',
        ),
    ]

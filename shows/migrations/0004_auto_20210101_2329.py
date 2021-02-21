# Generated by Django 3.1.4 on 2021-01-01 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0003_auto_20201230_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='tmdb_season_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='episode',
            name='tmdb_show',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shows.show'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='episode',
            unique_together={('tmdb_season_number', 'tmdb_episode_number', 'tmdb_show')},
        ),
        migrations.RemoveField(
            model_name='episode',
            name='tmdb_season',
        ),
    ]
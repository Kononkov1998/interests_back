# Generated by Django 3.1.2 on 2020-10-29 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20201029_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermovie',
            name='spent_time',
        ),
        migrations.AddField(
            model_name='movie',
            name='tmdb_runtime',
            field=models.IntegerField(default=89),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.1.4 on 2021-01-02 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0006_auto_20210102_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='tmdb_backdrop_path',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
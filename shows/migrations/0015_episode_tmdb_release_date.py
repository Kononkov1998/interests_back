# Generated by Django 3.1.5 on 2021-01-30 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0014_auto_20210130_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='tmdb_release_date',
            field=models.DateTimeField(null=True),
        ),
    ]

# Generated by Django 3.1.2 on 2020-10-29 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20201029_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='imdb_id',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
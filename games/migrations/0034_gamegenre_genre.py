# Generated by Django 3.1.4 on 2021-01-04 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0033_auto_20201208_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('rawg_id', models.IntegerField(primary_key=True, serialize=False)),
                ('rawg_name', models.CharField(max_length=100)),
                ('rawg_slug', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.genre')),
            ],
            options={
                'unique_together': {('game', 'genre')},
            },
        ),
    ]

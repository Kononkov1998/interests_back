# Generated by Django 3.1 on 2020-08-09 08:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0003_usergame'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserGame',
            new_name='UserGameScore',
        ),
        migrations.AlterField(
            model_name='game',
            name='hltb_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='hltb_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

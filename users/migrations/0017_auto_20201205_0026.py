# Generated by Django 3.1.2 on 2020-12-04 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_userpasswordtoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpasswordtoken',
            old_name='restore_token',
            new_name='reset_token',
        ),
    ]

# Generated by Django 3.1.5 on 2021-01-30 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0035_auto_20210124_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamelog',
            name='action_result',
            field=models.CharField(max_length=3000),
        ),
    ]

# Generated by Django 3.1 on 2020-08-13 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0009_auto_20200814_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='hltb_name',
            field=models.CharField(blank=True, default='', max_length=200),
            preserve_default=False,
        ),
    ]

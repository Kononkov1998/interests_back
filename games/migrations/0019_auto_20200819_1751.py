# Generated by Django 3.1 on 2020-08-19 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0018_auto_20200815_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergame',
            name='status',
            field=models.CharField(choices=[('playing', 'Играю'), ('completed', 'Прошел'), ('stopped', 'Дропнул'), ('going', 'Буду играть'), ('not played', 'Не играл')], max_length=30),
        ),
    ]
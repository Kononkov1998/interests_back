# Generated by Django 3.1.2 on 2020-10-14 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0023_auto_20200904_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergame',
            name='status',
            field=models.CharField(choices=[('playing', 'Играю'), ('completed', 'Прошел'), ('stopped', 'Дропнул'), ('going', 'Буду играть'), ('not played', 'Не играл')], default='not played', max_length=30),
        ),
    ]
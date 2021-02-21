# Generated by Django 3.1.1 on 2020-09-04 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0022_auto_20200819_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamelog',
            name='action_type',
            field=models.CharField(choices=[('score', 'Score changed'), ('review', 'Review changed'), ('status', 'Status changed'), ('spent_time', 'Spent time changed')], max_length=30),
        ),
    ]

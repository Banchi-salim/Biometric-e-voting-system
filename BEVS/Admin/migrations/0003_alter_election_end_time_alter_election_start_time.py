# Generated by Django 4.2.16 on 2024-12-17 00:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0002_alter_election_end_time_alter_election_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='end_time',
            field=models.TimeField(default=datetime.time(2, 38, 47, 232469)),
        ),
        migrations.AlterField(
            model_name='election',
            name='start_time',
            field=models.TimeField(default=datetime.time(0, 38, 47, 232453)),
        ),
    ]
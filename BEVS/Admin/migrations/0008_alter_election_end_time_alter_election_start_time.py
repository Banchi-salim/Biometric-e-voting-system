# Generated by Django 4.2.16 on 2024-12-17 01:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0007_alter_election_end_time_alter_election_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='end_time',
            field=models.TimeField(default=datetime.time(3, 16, 19, 760542)),
        ),
        migrations.AlterField(
            model_name='election',
            name='start_time',
            field=models.TimeField(default=datetime.time(1, 16, 19, 760526)),
        ),
    ]
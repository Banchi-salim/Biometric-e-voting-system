# Generated by Django 5.1.4 on 2025-01-01 07:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0011_remove_voter_fingerprint_voter_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voter',
            name='user',
        ),
        migrations.AlterField(
            model_name='election',
            name='end_time',
            field=models.TimeField(default=datetime.time(9, 45, 7, 312274)),
        ),
        migrations.AlterField(
            model_name='election',
            name='start_time',
            field=models.TimeField(default=datetime.time(7, 45, 7, 312274)),
        ),
    ]

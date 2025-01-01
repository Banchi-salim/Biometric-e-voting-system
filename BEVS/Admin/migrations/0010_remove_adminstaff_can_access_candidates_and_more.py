# Generated by Django 4.2.16 on 2024-12-19 01:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0009_adminstaff_can_access_candidates_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminstaff',
            name='can_access_candidates',
        ),
        migrations.RemoveField(
            model_name='adminstaff',
            name='can_access_elections',
        ),
        migrations.RemoveField(
            model_name='adminstaff',
            name='can_access_reports',
        ),
        migrations.RemoveField(
            model_name='adminstaff',
            name='can_access_users',
        ),
        migrations.RemoveField(
            model_name='adminstaff',
            name='can_access_voters',
        ),
        migrations.AlterField(
            model_name='election',
            name='end_time',
            field=models.TimeField(default=datetime.time(3, 56, 5, 808133)),
        ),
        migrations.AlterField(
            model_name='election',
            name='start_time',
            field=models.TimeField(default=datetime.time(1, 56, 5, 808119)),
        ),
    ]
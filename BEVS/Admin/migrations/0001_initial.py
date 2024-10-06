# Generated by Django 5.1 on 2024-10-06 22:37

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='candidates/')),
                ('votes', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Election', max_length=100)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('start_time', models.TimeField(default=datetime.time(22, 36, 59, 453490))),
                ('end_time', models.TimeField(default=datetime.time(0, 36, 59, 453490))),
            ],
        ),
        migrations.CreateModel(
            name='Ongoing_Election',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('candidates', models.ManyToManyField(to='Admin.candidate')),
                ('election', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Admin.election')),
            ],
        ),
    ]
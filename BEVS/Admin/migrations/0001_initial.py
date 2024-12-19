# Generated by Django 4.2.16 on 2024-12-16 22:16

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('profile_image', models.ImageField(upload_to='profile_images/')),
                ('access_control', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='candidates/')),
                ('votes', models.PositiveIntegerField(default=0)),
                ('color', models.CharField(default='ffffff', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Election', max_length=100)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('start_time', models.TimeField(default=datetime.time(22, 16, 42, 726173))),
                ('end_time', models.TimeField(default=datetime.time(0, 16, 42, 726426))),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('address', models.TextField()),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='voter_images/')),
                ('fingerprint', models.BinaryField(blank=True, null=True)),
                ('elections', models.ManyToManyField(related_name='voters', to='Admin.election')),
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
        migrations.CreateModel(
            name='ElectionReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_voters', models.IntegerField(default=0)),
                ('total_votes_cast', models.IntegerField(default=0)),
                ('election', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='Admin.election')),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='election',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin.election'),
        ),
    ]
from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone


class Election(models.Model):
    name = models.CharField(max_length=100, default='Election')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now().time())
    end_time = models.TimeField(default=(timezone.now() + timedelta(hours=2)).time())

    def __str__(self):
        return self.name


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='candidates/')
    votes = models.PositiveIntegerField(default=0)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    color = models.CharField(max_length=7)  # HEX color code

    def __str__(self):
        return self.name


class Ongoing_Election(models.Model):
    title = models.CharField(max_length=255)
    candidates = models.ManyToManyField('Candidate')  # Assuming you have a Candidate model
    election = models.OneToOneField('Election', on_delete=models.CASCADE)  # Link to the Election model
    is_active = models.BooleanField(default=False)  # Default is False, but it can be auto-updated

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically set is_active based on current time and election date/time range
        current_time = timezone.now()
        if self.election.start_date <= current_time.date() <= self.election.end_date:
            if (self.election.start_time <= current_time.time() <= self.election.end_time):
                self.is_active = True
            else:
                self.is_active = False
        else:
            self.is_active = False

        super(Ongoing_Election, self).save(*args, **kwargs)


class Voter(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateField()
    address = models.TextField()
    profile_image = models.ImageField(upload_to='voter_images/', null=True, blank=True)
    fingerprint = models.BinaryField(null=True, blank=True)  # Store raw fingerprint data

    def __str__(self):
        return self.name


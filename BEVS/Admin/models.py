from datetime import timedelta, timezone
from django.db import models

from .task import *


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='candidates/')
    votes = models.PositiveIntegerField(default=0)
    election = models.ForeignKey('Election', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Election(models.Model):
    name = models.CharField(max_length=100, default='Election')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now().time(), null=True, blank=True)
    end_time = models.TimeField(default=(timezone.now() + timedelta(hours=2)).time(), null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Get the current date and time
        current_time = timezone.now()

        # Combine start_date and start_time into one datetime object
        start_datetime = timezone.make_aware(timezone.datetime.combine(self.start_date, self.start_time))

        # Combine end_date and end_time into one datetime object
        end_datetime = timezone.make_aware(timezone.datetime.combine(self.end_date, self.end_time))

        # Check if the current time is within the election start and end time
        if start_datetime <= current_time <= end_datetime:
            self.is_active = True
        else:
            self.is_active = False

        # Call the parent class's save method
        super(Election, self).save(*args, **kwargs)

        # If election hasn't started, schedule the task to activate it at start time
        if not self.is_active:
            self.schedule_election_activation(start_datetime)

    def schedule_election_activation(self, start_datetime):
        """
        Schedules the `activate_election` task to run at the election start time.
        """
        time_until_start = start_datetime - timezone.now()
        # Convert the time difference to seconds
        time_until_start_seconds = time_until_start.total_seconds()

        # Schedule the task to run at the start time of the election
        activate_election.apply_async((self.id,), countdown=time_until_start_seconds)



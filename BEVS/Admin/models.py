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
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True)
    color = models.CharField(max_length=7, default="ffffff")  # HEX color code

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
    elections = models.ManyToManyField('Election', related_name="voters")  # Many-to-Many Relationship

    def __str__(self):
        return self.name



class AdminStaff(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/')
    access_control = models.JSONField(default=list)  # Stores selected checkboxes as JSON

    def __str__(self):
        return self.name


class ElectionReport(models.Model):
    election = models.OneToOneField(Election, on_delete=models.CASCADE, related_name="report")
    total_voters = models.IntegerField(default=0)  # To store total registered voters for the election
    total_votes_cast = models.IntegerField(default=0)  # To store total votes cast in the election

    def __str__(self):
        return f"Report for {self.election.name}"

    def calculate_total_votes_cast(self):
        """Calculate the total votes cast by summing up candidate votes."""
        return sum(candidate.votes for candidate in self.election.candidate_set.all())

    def calculate_total_voters(self):
        """Calculate the total number of registered voters."""
        # You can further filter voters based on election criteria if needed
        return Voter.objects.count()  # Adjust this query if voters are election-specific

    def save(self, *args, **kwargs):
        # Automatically calculate and save total votes cast and total voters
        self.total_votes_cast = self.calculate_total_votes_cast()
        self.total_voters = self.calculate_total_voters()
        super(ElectionReport, self).save(*args, **kwargs)



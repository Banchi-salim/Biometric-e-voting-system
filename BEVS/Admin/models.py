from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils import timezone


class Election(models.Model):
    name = models.CharField(max_length=100, default='Election')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now().time())
    end_time = models.TimeField(default=(timezone.now() + timedelta(hours=2)).time())

    def __str__(self):
        return self.name

    @transaction.atomic
    def save(self, *args, **kwargs):
        # Save the Election first
        super().save(*args, **kwargs)
        ElectionReport.objects.create(election=self)

        # Check if an Ongoing_Election already exists for this Election
        existing_ongoing = Ongoing_Election.objects.filter(election=self).first()

        if not existing_ongoing:
            # Deactivate any existing active Ongoing_Election
            Ongoing_Election.objects.filter(is_active=True).update(is_active=False)

            # Create the corresponding Ongoing_Election model
            Ongoing_Election.objects.create(
                title=f"{self.name} - Ongoing",
                election=self,
                is_active=False
            )


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='candidates/', null=True, blank=True)
    votes = models.PositiveIntegerField(default=0)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True)
    color = models.CharField(max_length=7, default="ffffff")  # HEX color code

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Save the candidate first
        super().save(*args, **kwargs)

        # If the candidate is associated with an election, add to Ongoing_Election
        if self.election:
            try:
                ongoing_election = Ongoing_Election.objects.get(election=self.election)
                ongoing_election.candidates.add(self)
            except Ongoing_Election.DoesNotExist:
                # If no Ongoing_Election exists for this election, create one
                ongoing_election = Ongoing_Election.objects.create(
                    title=f"{self.election.name} - Ongoing",
                    election=self.election
                )
                ongoing_election.candidates.add(self)


class Ongoing_Election(models.Model):
    title = models.CharField(max_length=255)
    candidates = models.ManyToManyField('Candidate')  # Assuming you have a Candidate model
    election = models.OneToOneField('Election', on_delete=models.CASCADE)  # Link to the Election model
    is_active = models.BooleanField(default=False)  # Default is False, updated automatically

    def __str__(self):
        return self.title

    from datetime import datetime, date

    def save(self, *args, **kwargs):
        current_time = datetime.now()

        # Convert start_date to datetime.date if it's a string
        if isinstance(self.election.start_date, str):
            try:
                start_date = datetime.strptime(self.election.start_date, '%Y-%m-%d').date()
            except ValueError:
                # Try alternative date formats if needed
                start_date = datetime.strptime(self.election.start_date, '%m/%d/%Y').date()
        else:
            start_date = self.election.start_date

        # Convert end_date to datetime.date if it's a string
        if isinstance(self.election.end_date, str):
            try:
                end_date = datetime.strptime(self.election.end_date, '%Y-%m-%d').date()
            except ValueError:
                # Try alternative date formats if needed
                end_date = datetime.strptime(self.election.end_date, '%m/%d/%Y').date()
        else:
            end_date = self.election.end_date

        # Convert string times to datetime.time if necessary
        if isinstance(self.election.start_time, str):
            start_time = datetime.strptime(self.election.start_time, '%H:%M').time()
        else:
            start_time = self.election.start_time

        if isinstance(self.election.end_time, str):
            end_time = datetime.strptime(self.election.end_time, '%H:%M').time()
        else:
            end_time = self.election.end_time

        # Compare dates and times
        if (start_date <= current_time.date() <= end_date and
                start_time <= current_time.time() <= end_time):
            self.is_active = True
        else:
            self.is_active = False

        super().save(*args, **kwargs)

"""
class Voter(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateField()
    address = models.TextField()
    email = models.EmailField(null=True)
    profile_image = models.ImageField(upload_to='voter_images/', null=True, blank=True)
    fingerprint = models.BinaryField(null=True, blank=True)  # Store raw fingerprint data
    elections = models.ManyToManyField('Election', related_name="voters")  # Many-to-Many Relationship

    def __str__(self):
        return self.name
"""

class AdminStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
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


from django.db import models
from django.contrib.auth.models import User
import cv2
import numpy as np
from sklearn.metrics import mean_squared_error
import base64
import io


class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    address = models.TextField()
    email = models.EmailField(null=True)
    profile_image = models.ImageField(upload_to='voter_images/', null=True, blank=True)
    fingerprint_image = models.ImageField(
        upload_to='fingerprints/',
        null=True,
        blank=True
    )
    fingerprint_template = models.TextField(
        null=True,
        blank=True,
        help_text="Processed fingerprint template data"
    )
    elections = models.ManyToManyField('Election', related_name="voters")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def verify_fingerprint(self, fingerprint_base64):
        try:
            # Remove the data URL prefix if present
            if ',' in fingerprint_base64:
                fingerprint_base64 = fingerprint_base64.split(',')[1]

            # Decode base64 to image
            current_image_data = base64.b64decode(fingerprint_base64)
            current_image = cv2.imdecode(
                np.frombuffer(current_image_data, np.uint8),
                cv2.IMREAD_GRAYSCALE
            )

            # Get stored fingerprint
            if not self.fingerprint_image:
                return False, "No stored fingerprint found"

            stored_image = cv2.imread(self.fingerprint_image.path, cv2.IMREAD_GRAYSCALE)

            if stored_image is None:
                return False, "Could not read stored fingerprint"

            # Resize current image to match stored image dimensions
            current_image_resized = cv2.resize(
                current_image,
                (stored_image.shape[1], stored_image.shape[0])
            )

            # Calculate similarity
            mse = mean_squared_error(
                stored_image.flatten(),
                current_image_resized.flatten()
            )

            # Threshold for fingerprint match (adjust as needed)
            if mse < 500:  # Lower threshold means stricter matching
                return True, "Fingerprint verified successfully"

            return False, "Fingerprint verification failed"

        except Exception as e:
            return False, str(e)

    def __str__(self):
        return self.name

# The UserProfile model can be removed since its functionality is now in the Voter model
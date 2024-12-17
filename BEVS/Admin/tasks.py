from celery import shared_task
from django.utils import timezone
from django.apps import apps


@shared_task
def manage_election_status():
    Election = apps.get_model('Admin', 'Election')
    OngoingElection = apps.get_model('Admin', 'OngoingElection')

    current_time = timezone.now()

    # Loop through all elections to manage their status
    for election in Election.objects.all():
        start_datetime = timezone.make_aware(
            timezone.datetime.combine(election.start_date, election.start_time)
        )
        end_datetime = timezone.make_aware(
            timezone.datetime.combine(election.end_date, election.end_time)
        )

        try:
            # Get or create the OngoingElection record for the election
            ongoing_election, created = OngoingElection.objects.get_or_create(election=election)

            # Check election time to determine status
            if start_datetime <= current_time <= end_datetime:
                # Activate the election if it falls within the current time
                ongoing_election.is_active = True
            elif current_time > end_datetime:
                # Deactivate if the current time has passed the end time
                ongoing_election.is_active = False
            else:
                # Deactivate if the election hasn't started yet
                ongoing_election.is_active = False

            # Save changes to the OngoingElection instance
            ongoing_election.save()

        except Exception as e:
            print(f"Error managing election status for {election.name}: {e}")

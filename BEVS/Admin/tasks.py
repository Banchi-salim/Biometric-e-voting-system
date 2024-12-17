from celery import shared_task
from django.utils import timezone
from django.apps import apps


@shared_task
def manage_election_status():
    Election = apps.get_model('Admin', 'Election')
    OngoingElection = apps.get_model('Admin', 'OngoingElection')

    current_time = timezone.now()

    # Activate or deactivate elections based on time
    for election in Election.objects.all():
        start_datetime = timezone.make_aware(
            timezone.datetime.combine(election.start_date, election.start_time)
        )
        end_datetime = timezone.make_aware(
            timezone.datetime.combine(election.end_date, election.end_time)
        )

        try:
            ongoing_election = OngoingElection.objects.get(election=election)
        except OngoingElection.DoesNotExist:
            # If no ongoing election exists, skip
            continue

        if start_datetime <= current_time <= end_datetime:
            # Activate the election if it falls within the current time
            ongoing_election.is_active = True
        else:
            # Deactivate otherwise
            ongoing_election.is_active = False

        ongoing_election.save()

from celery import shared_task
from django.utils import timezone
from django.apps import apps


@shared_task
def activate_election(election_id):
    Election = apps.get_model('Admin', 'Election')
    try:
        election = Election.objects.get(id=election_id)
        current_time = timezone.now()
        start_datetime = timezone.make_aware(timezone.datetime.combine(election.start_date, election.start_time))

        # If the current time is past the start time, activate the election
        if current_time >= start_datetime:
            election.is_active = True
            election.save()
    except Election.DoesNotExist:
        pass  # Election does not exist, handle accordingly


@shared_task
def deactivate_election(election_id):
    Election = apps.get_model('Admin', 'Election')
    try:
        election = Election.objects.get(id=election_id)
        current_time = timezone.now()
        end_datetime = timezone.make_aware(timezone.datetime.combine(election.end_date, election.end_time))

        # If the current time is past the end time, deactivate the election
        if current_time >= end_datetime:
            election.is_active = False
            election.save()
    except Election.DoesNotExist:
        pass  # Election does not exist, handle accordingly

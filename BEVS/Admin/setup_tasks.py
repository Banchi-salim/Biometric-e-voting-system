from django_celery_beat.models import PeriodicTask, IntervalSchedule
from datetime import timedelta
import json

def setup_periodic_task():
    # Create the schedule if it doesn't exist
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,  # Run every 10 seconds
        period=IntervalSchedule.SECONDS,  # Options: SECONDS, MINUTES, HOURS, DAYS, WEEKS
    )

    # Create the periodic task if it doesn't exist
    task_name = 'manage_election_status'
    if not PeriodicTask.objects.filter(name=task_name).exists():
        PeriodicTask.objects.create(
            interval=schedule,  # Use the schedule
            name=task_name,  # Unique name for the task
            task='Admin.tasks.manage_election_status',  # Full task path
            args=json.dumps([]),  # Arguments for the task (empty list for none)
            kwargs=json.dumps({}),  # Keyword arguments for the task
        )

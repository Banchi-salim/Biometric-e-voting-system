import logging
from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.apps import apps
import pytz

# Set up logger
logger = logging.getLogger(__name__)



@shared_task
def manage_election_status():
    """
    Celery task to manage election status based on start and end times.
    Updates the is_active flag for ongoing elections.
    """
    Election = apps.get_model('Admin', 'Election')
    Ongoing_Election = apps.get_model('Admin', 'Ongoing_Election')

    # Set timezone to Africa/Lagos (Nigerian timezone)
    local_tz = pytz.timezone('Africa/Lagos')  # Nigeria's timezone

    try:
        ongoing_elections = Ongoing_Election.objects.all()
        logger.info(f"Processing {ongoing_elections.count()} ongoing elections")

        for election in ongoing_elections:
            try:
                main = Election.objects.get(id=election.election_id)

                # Get current time and convert to local timezone
                current_time = timezone.now().astimezone(local_tz) + timedelta(hours=1)

                # Make start and end times timezone-aware in local timezone
                start_datetime = timezone.make_aware(
                    timezone.datetime.combine(main.start_date, main.start_time),
                    timezone=local_tz
                )
                end_datetime = timezone.make_aware(
                    timezone.datetime.combine(main.end_date, main.end_time),
                    timezone=local_tz
                )

                # Store previous state for comparison
                previous_state = election.is_active

                # Log time details for debugging
                logger.debug(f"""
                    Election: {main.name}
                    Current Time: {current_time}
                    Start Time: {start_datetime}
                    End Time: {end_datetime}
                """)

                # Update status based on time comparison
                if start_datetime <= current_time <= end_datetime:
                    election.is_active = True
                    election.save()
                    status_msg = "activated"
                else:
                    election.is_active = False
                    election.save()
                    status_msg = "deactivated (past end time)" if current_time > end_datetime else "deactivated (before start time)"

                # Only save and log if there's a state change
                if previous_state != election.is_active:
                    election.save()
                    logger.warning(f"Election '{main.name}' status changed to {status_msg}")
                    logger.info(f"""
                        Status Change Details:
                        - Election: {main.name}
                        - Previous State: {previous_state}
                        - New State: {election.is_active}
                        - Current Time: {current_time}
                        - Start Time: {start_datetime}
                        - End Time: {end_datetime}
                    """)

            except Election.DoesNotExist:
                logger.error(f"Election with ID {election.election_id} not found")
            except Exception as e:
                logger.error(f"Error processing election {election.election_id}: {str(e)}", exc_info=True)

        return "Election status update completed successfully"

    except Exception as e:
        logger.error(f"Fatal error in manage_election_status task: {str(e)}", exc_info=True)
        raise

import pytz
from datetime import timedelta
from django.utils import timezone
from django.apps import apps
import logging

# Set up logging to print to the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def manage_election_status_1():
    """
    Function to manage election status based on start and end times.
    Updates the is_active flag for ongoing elections and logs information to the terminal.
    """
    Election = apps.get_model('Admin', 'Election')
    Ongoing_Election = apps.get_model('Admin', 'Ongoing_Election')

    # Set timezone to Africa/Lagos (Nigerian timezone)
    local_tz = pytz.timezone('Africa/Lagos')  # Nigeria's timezone

    try:
        ongoing_elections = Ongoing_Election.objects.all()
        logger.info(f"Processing {ongoing_elections.count()} ongoing elections")

        for election in ongoing_elections:
            try:
                main = Election.objects.get(id=election.election_id)

                # Get current time and convert to local timezone
                current_time = timezone.now().astimezone(local_tz) + timedelta(hours=1)

                # Make start and end times timezone-aware in local timezone
                start_datetime = timezone.make_aware(
                    timezone.datetime.combine(main.start_date, main.start_time),
                    timezone=local_tz
                )
                end_datetime = timezone.make_aware(
                    timezone.datetime.combine(main.end_date, main.end_time),
                    timezone=local_tz
                )

                # Store previous state for comparison
                previous_state = election.is_active

                # Log time details for debugging
                logger.info(f"""
                    Election: {main.name}
                    Current Time: {current_time}
                    Start Time: {start_datetime}
                    End Time: {end_datetime}
                """)

                # Update status based on time comparison
                if start_datetime <= current_time <= end_datetime:
                    election.is_active = True
                    election.save()
                    status_msg = "activated"
                else:
                    election.is_active = False
                    election.save()
                    status_msg = "deactivated (past end time)" if current_time > end_datetime else "deactivated (before start time)"

                # Only save and log if there's a state change
                if previous_state != election.is_active:
                    election.save()
                    logger.info(f"Election '{main.name}' status changed to {status_msg}")
                    logger.info(f"""
                        Status Change Details:
                        - Election: {main.name}
                        - Previous State: {previous_state}
                        - New State: {election.is_active}
                        - Current Time: {current_time}
                        - Start Time: {start_datetime}
                        - End Time: {end_datetime}
                    """)

            except Election.DoesNotExist:
                logger.error(f"Election with ID {election.election_id} not found")
            except Exception as e:
                logger.error(f"Error processing election {election.election_id}: {str(e)}", exc_info=True)

        logger.info("Election status update completed successfully")
        return "Election status update completed successfully"

    except Exception as e:
        logger.error(f"Fatal error in manage_election_status function: {str(e)}", exc_info=True)
        raise

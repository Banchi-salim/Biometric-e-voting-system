from Admin.models import Ongoing_Election, Election
from django.utils import timezone

# Fetch all ongoing elections
ongoing_elections = Ongoing_Election.objects.all()
print(ongoing_elections)
# Loop through each election one by one
for election in ongoing_elections:
    try:
        main = Election.objects.get(id=election.election_id)
        current_time = timezone.now()

        start_datetime = timezone.make_aware(
            timezone.datetime.combine(main.start_date, main.start_time)
        )
        end_datetime = timezone.make_aware(
            timezone.datetime.combine(main.end_date, main.end_time)
        )

        previous_state = election.is_active

        # Update status based on time comparison
        if start_datetime <= current_time <= end_datetime:
            election.is_active = True
            election.save()
            status_msg = "activated"
            print(status_msg)
        else:
            election.is_active = False
            election.save()
            status_msg = "deactivated (past end time)" if current_time > end_datetime else "deactivated (before start time)"
            print(status_msg)
        if previous_state != election.is_active:
            election.save()
            print(f"Election '{main.name}' {status_msg}")


    except Election.DoesNotExist:
        print(f"Election with ID {election.election_id} not found")
    except Exception as e:
        print(f"Error processing election {election.election_id}: {str(e)}")

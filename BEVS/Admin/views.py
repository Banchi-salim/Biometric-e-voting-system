import csv
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
# from django.utils.baseconv import base64

from .models import *


def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            # Use namespaced URL name
            next_url = request.GET.get('next', reverse('admin:admin_dashboard'))
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials or not an admin.')

    return render(request, 'Admin/login.html')


@login_required(login_url='admin:admin_login')
def admin_dashboard(request):
    elections = Ongoing_Election.objects.filter(is_active=True)
    return render(request, 'Admin/Home.html', {'elections': elections})


def vote_data(request, election_id):
    election = Election.objects.get(id=election_id)
    vote_counts = {
        candidate.name: candidate.votes for candidate in election.candidates.all()
    }
    return JsonResponse(vote_counts)


def register_election(request):
    if request.method == 'POST':
        election_name = request.POST['election_name']
        start_date = request.POST.get('start_date', timezone.now().date())
        end_date = request.POST['end_date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        # Create the new election object
        Election.objects.create(
            name=election_name,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time
        )
        messages.success(request, 'Election created successfully.')
        return redirect('admin:register_election')  # Redirect to the same form or dashboard
    return render(request, 'Admin/Reg_election.html')


def add_candidate(request):
    # Fetch all elections from the database
    elections = Election.objects.all()

    if request.method == 'POST':
        candidate_name = request.POST.get('candidate_name')
        election_id = request.POST.get('election')
        color = request.POST.get('color')
        candidate_image = request.FILES.get('candidate_image')

        # You can now process the data and store it in the database
        election = Election.objects.get(id=election_id)

        # Save candidate data
        candidate = Candidate(
            name=candidate_name,
            election=election,
            color=color,
            image=candidate_image  # Assuming you've added an image field to the Candidate model
        )
        candidate.save()

        messages.success(request, "Candidate added successfully!")
        return redirect('admin:register_candidates')  # Redirect back to the form page or another page

    return render(request, 'admin/reg_candidates.html', {'elections': elections})


def register_voter(request):
    if request.method == 'POST':
        # Get voter data from the form
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        address = request.POST.get('address')
        profile_image = request.FILES.get('profile_image')
        fingerprint_data = request.POST.get('fingerprint_data')  # Fingerprint data (image/template)

        # Decode fingerprint data if required
        if fingerprint_data:
            fingerprint_data = ""  # Example placeholder: base64.b64decode(fingerprint_data)

        try:
            # Save the voter data along with the fingerprint data
            voter = Voter(
                name=name,
                dob=dob,
                address=address,
                email=email,
                profile_image=profile_image,
                fingerprint=fingerprint_data
            )
            voter.save()  # Save voter instance to the database

            # Send mail after saving the voter
            send_mail(
                subject=f"Successful Registration On BEVS",
                message=f"Hi {name},\n\n"
                        f"You have successfully been registered on BEVS:\n\n"
                        f"Name: {name}\n"
                        f"DOB: {dob}\n"
                        f"Address: {address}\n\n"
                        f"You will be updated regularly.",
                from_email='no-reply@ncdc.gov.ng',
                recipient_list=[email],
                fail_silently=True
            )

            messages.success(request, "Voter registration successful!")
            return redirect('register_voter')  # Redirect back to the registration page

        except Exception as e:
            print(f"Error during voter registration: {e}")
            messages.error(request, "An error occurred during registration. Please try again.")

    return render(request, 'admin/reg_voters.html')


def add_admin_staff(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        username = request.POST.get('username')
        password = request.POST.get('password')
        access_control = request.POST.getlist('access_control')  # Get selected checkboxes

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()

        # Create staff profile
        profile_image = request.FILES.get('profile_image')
        staff_profile = AdminStaff.objects.create(
            user=user,
            dob=dob,
            phone=phone,
            address=address,
            profile_image=profile_image,
            access_control=access_control,
        )

        staff_profile.save()

        return redirect('admin:staff_list')  # Redirect to the staff list page.

    return render(request, 'Admin/add_admin_staff.html')



def election_reports(request):
    # Get all completed elections and their reports
    reports = ElectionReport.objects.select_related('election').all()
    return render(request, 'Admin/election_reports.html', {'reports': reports})


def download_report(request, report_id):
    report = get_object_or_404(ElectionReport, id=report_id)
    candidates = Candidate.objects.filter(election=report.election)

    # Create the CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report.election.name}_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Election Name', report.election.name])
    writer.writerow(['Election Date', report.election.start_date, 'to', report.election.end_date])
    writer.writerow(['Total Voters', report.total_voters])
    writer.writerow(['Total Votes Cast', report.total_votes_cast])
    writer.writerow([])  # Blank row
    writer.writerow(['Candidate Name', 'Votes'])

    for candidate in candidates:
        writer.writerow([candidate.name, candidate.votes])

    return response


def logout_view(request):
    """
    Log the user out and redirect to the login page (or home page).
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('admin:admin_login')


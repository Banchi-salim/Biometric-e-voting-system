from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
#from django.utils.baseconv import base64

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
        return redirect('Admin/Reg_election.html')  # Redirect to the same form or dashboard
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
        return redirect('add_candidate')  # Redirect back to the form page or another page

    return render(request, 'admin/reg_candidates.html', {'elections': elections})


def register_voter(request):
    if request.method == 'POST':
        # Get voter data from the form
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        profile_image = request.FILES.get('profile_image')
        fingerprint_data = request.POST.get('fingerprint_data')  # The fingerprint data (image/template)

        # Decode the fingerprint data (if it's base64 encoded)
        # Here, we're assuming the fingerprint data is base64-encoded
        if fingerprint_data:
            fingerprint_data = base64.b64decode(fingerprint_data)

        # Save the voter data along with the fingerprint data
        voter = Voter(
            name=name,
            dob=dob,
            address=address,
            profile_image=profile_image,
            fingerprint=fingerprint_data  # Store the raw fingerprint data in the model
        )
        voter.save()

        messages.success(request, "Voter registration successful!")
        return redirect('register_voter')  # Redirect back to the registration page

    return render(request, 'admin/reg_voters.html')
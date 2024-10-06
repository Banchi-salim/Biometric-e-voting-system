from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

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

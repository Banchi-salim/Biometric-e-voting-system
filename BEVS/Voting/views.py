from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from Admin.models import Ongoing_Election, Candidate, Voter


def voter_login(request):
    """Render the fingerprint login page."""
    return render(request, 'Voting/login.html')


def verify_fingerprint(request):
    """Verify fingerprint data sent from the frontend."""
    if request.method == 'POST':
        # Simulate fingerprint data verification (replace this with real fingerprint matching logic)
        # In a real scenario, you would extract and compare the fingerprint data here.
        fingerprint_data = request.body  # Get raw fingerprint data
        voter = Voter.objects.filter(fingerprint=fingerprint_data).first()

        if voter:
            # Log in the voter (session management)
            request.session['voter_id'] = voter.id
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def voting_page(request):
    ongoing_elections = Ongoing_Election.objects.filter(is_active=True).prefetch_related('candidates')
    return render(request, 'Voting/voting.html', {'ongoing_elections': ongoing_elections})


def submit_votes(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('vote_'):
                election_id = key.split('_')[1]
                candidate_id = value
                candidate = Candidate.objects.get(id=candidate_id)
                candidate.votes += 1
                candidate.save()
        messages.success(request, 'Your votes have been submitted successfully!')
        return redirect('election_monitoring')
    return redirect('voting_page')


def election_monitoring(request):
    ongoing_elections = Ongoing_Election.objects.filter(is_active=True)
    return render(request, 'Voting/election_monitoring.html', {'ongoing_elections': ongoing_elections})

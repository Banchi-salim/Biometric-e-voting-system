from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from Admin.models import Ongoing_Election, Candidate, Voter
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate
from .models import *
import base64
import numpy as np
import cv2
from skimage import io
import numpy as np
from sklearn.metrics import mean_squared_error
from django.core.files.base import ContentFile

def voter_login(request):
    """Render the fingerprint login page."""
    return render(request, 'Voting/login.html')


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



@csrf_protect
def verify_fingerprint(request):
    if request.method == 'POST':
        try:
            # Remove the data URL prefix
            base64_image = request.POST.get('fingerprint_image').split(',')[1]

            # Decode base64 to image
            current_image_data = base64.b64decode(base64_image)
            current_image = io.imread(current_image_data)

            # Retrieve user's stored fingerprint
            profile = Voter.objects.get(user=request.user)
            stored_image_path = profile.fingerprint_image.path
            stored_image = cv2.imread(stored_image_path, cv2.IMREAD_GRAYSCALE)
            current_image_gray = cv2.cvtColor(current_image, cv2.COLOR_RGB2GRAY)

            # Simple comparison (you'd want a more sophisticated method in production)
            if stored_image is not None:
                # Resize images to same dimension
                current_image_resized = cv2.resize(current_image_gray, (stored_image.shape[1], stored_image.shape[0]))

                # Calculate similarity (lower MSE means more similar)
                mse = mean_squared_error(stored_image.flatten(), current_image_resized.flatten())

                # Threshold for fingerprint match (adjust as needed)
                if mse < 500:  # Lower threshold means stricter matching
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Fingerprint verified successfully'
                    })

            return JsonResponse({
                'status': 'error',
                'message': 'Fingerprint verification failed'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })


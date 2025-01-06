from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from Admin.models import Ongoing_Election, Candidate, Voter
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate
from skimage.metrics import structural_similarity
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
            # Get the uploaded fingerprint image file and registration number
            fingerprint_file = request.FILES.get('fingerprint_image')
            registration_number = request.POST.get('registration_number')

            if not fingerprint_file:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No fingerprint image provided'
                })

            if not registration_number:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Registration number is required'
                })

            # Retrieve the voter's profile using the registration number
            profile = get_object_or_404(Voter, registration_number=registration_number)

            # Read the uploaded fingerprint image
            current_image_data = fingerprint_file.read()
            current_image = cv2.imdecode(
                np.frombuffer(current_image_data, np.uint8),
                cv2.IMREAD_GRAYSCALE
            )
            fingerprint_file.seek(0)  # Reset file pointer for potential future reads

            # Get the stored fingerprint image
            if not profile.fingerprint_image:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No stored fingerprint found for this user'
                })

            # Read the stored fingerprint image
            stored_image = cv2.imread(profile.fingerprint_image.path, cv2.IMREAD_GRAYSCALE)

            if stored_image is None:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Could not read stored fingerprint'
                })

            # Resize current image to match stored image dimensions
            current_image_resized = cv2.resize(
                current_image,
                (stored_image.shape[1], stored_image.shape[0])
            )

            # Calculate similarity using MSE and SSIM
            mse = mean_squared_error(stored_image.flatten(), current_image_resized.flatten())
            ssim_score = structural_similarity(stored_image, current_image_resized)

            # Verification thresholds (adjust these based on accuracy requirements)
            if mse < 500 and ssim_score > 0.5:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Fingerprint verified successfully',
                    'redirect_url': '/dashboard/'  # Adjust this as per your redirection requirements
                })

            return JsonResponse({
                'status': 'error',
                'message': f'Fingerprint verification failed (MSE: {mse:.2f}, SSIM: {ssim_score:.2f})'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error during verification: {str(e)}'
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json


@require_http_methods(["POST"])
def validate_registration(request):
    data = json.loads(request.body)
    reg_number = data.get('registration_number')

    try:
        # Add your validation logic here
        # For example:
        voter = Voter.objects.filter(voter_reg_number=reg_number).first()
        if voter:
            return JsonResponse({
                'valid': True,
                'message': 'Registration number valid'
            })
        else:
            return JsonResponse({
                'valid': False,
                'message': 'Invalid registration number'
            })
    except Exception as e:
        return JsonResponse({
            'valid': False,
            'message': str(e)
        })
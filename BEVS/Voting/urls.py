from django.urls import path
from . import views

urlpatterns = [
    path('', views.voter_login, name='voter_login'),
    path('verify-fingerprint/', views.verify_fingerprint, name='verify_fingerprint'),
    path('voting/', views.voting_page, name='voting_page'),
    path('submit-votes/', views.submit_votes, name='submit_votes'),
    path('monitor-election/', views.election_monitoring, name='election_monitoring'),
    path('validate-registration/', views.validate_registration, name='validate_registration'),
]

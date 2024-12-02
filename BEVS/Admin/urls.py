from django.urls import path
from .views import admin_login_view, vote_data, admin_dashboard, register_election, add_candidate, register_voter

app_name = 'admin'
urlpatterns = [
    path('login/', admin_login_view, name='admin_login'),
    path('', admin_dashboard, name='admin_dashboard'),  # Changed from empty string
    path('vote-data/<int:election_id>/', vote_data, name='vote_data'),
    path('reg-election/', register_election, name='register_election'),
    path('reg-candidates/', add_candidate, name='register_candidates'),
    path('reg-voters/', register_voter, name='register_voters'),
]

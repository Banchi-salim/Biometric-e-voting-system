from django.urls import path
from .views import admin_login_view, vote_data, admin_dashboard, register_election

app_name = 'admin'
urlpatterns = [
    path('login/', admin_login_view, name='admin_login'),
    path('', admin_dashboard, name='admin_dashboard'),  # Changed from empty string
    path('vote-data/<int:election_id>/', vote_data, name='vote_data'),
    path('reg_election/', register_election, name='register_election')
]

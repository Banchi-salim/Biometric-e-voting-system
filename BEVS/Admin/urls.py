from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'admin'
urlpatterns = [
    path('login/', views.admin_login_view, name='admin_login'),
    path('', views.admin_dashboard, name='admin_dashboard'),  # Changed from empty string
    path('vote-data/<int:election_id>/', views.vote_data, name='vote_data'),
    path('reg-election/', views.register_election, name='register_election'),
    path('reg-candidates/', views.add_candidate, name='register_candidates'),
    path('reg-voters/', views.register_voter, name='register_voters'),
    path('add-admin-staff/', views.add_admin_staff, name='add_admin_staff'),
    path('election-reports/', views.election_reports, name='election_reports'),
    path('download-report/<int:report_id>/', views.download_report, name='download_report'),
    path('capture-print/', views.capture_print, name='capture_print'),
    path('logout/', views.logout_view, name='logout'),
]


# Serve media files for different folders.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Add manual mappings for other scattered folders:
    urlpatterns += static('/candidates/', document_root= settings.BASE_DIR / 'candidates')
    urlpatterns += static('/fingerprints/', document_root=settings.BASE_DIR / 'fingerprints')
    urlpatterns += static('/profile_images/', document_root=settings.BASE_DIR / 'profile_images')
    urlpatterns += static('/voter_images/', document_root=settings.BASE_DIR / 'voter_images')
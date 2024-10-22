from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from .models import *

class MyAdminSite(AdminSite):
    site_header = 'BioVote Secure Administration'
    site_title = 'BioVote Secure Admin Portal'
    index_title = 'Welcome to BioVote Secure Admin'

# Create an instance of your custom admin site
my_admin_site = MyAdminSite(name='Bevs_admin')

# Register your models with your custom admin site
my_admin_site.register(User)
my_admin_site.register(Group)
my_admin_site.register(Candidate)
my_admin_site.register(Election)




from datetime import datetime

from django.apps import AppConfig
import threading
import signal
import os

from django.utils import timezone
from django.utils.timezone import now


class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Admin'


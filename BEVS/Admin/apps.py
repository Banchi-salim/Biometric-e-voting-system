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

    def ready(self):
        from .setup_tasks import setup_periodic_task
        setup_periodic_task()
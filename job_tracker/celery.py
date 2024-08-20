import os

from celery import Celery

# set the default Django settings module for 'celery' app
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_tracker.settings.local")

app = Celery("job_tracker")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load tasks from all registered apps in INSTALLED_APPS
app.autodiscover_tasks()

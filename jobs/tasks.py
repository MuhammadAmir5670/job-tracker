from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import Job


@shared_task
def expire_jobs():
    fifteen_days_ago = timezone.now() - timedelta(days=15)

    expired_jobs = Job.objects.filter(created_at__gt=fifteen_days_ago)
    expired_jobs.update(status=Job.Status.EXPIRED)

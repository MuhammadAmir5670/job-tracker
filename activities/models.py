from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from core.models import TimeStampedModel
from jobs.models import Job


class ActivityType(TimeStampedModel):
    """Model definition for Activity."""

    name = models.CharField(max_length=250, unique=True)

    class Meta:
        """Meta definition for Activity."""

        verbose_name = "Activity Type"
        verbose_name_plural = "Activity Types"

    def __str__(self):
        """Unicode representation of Activity."""
        return self.name


class Activity(TimeStampedModel):
    """Model definition for Activity."""

    title = models.CharField(max_length=250)
    note = models.TextField()
    due_datetime = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.ForeignKey(
        ActivityType, to_field="name", db_column="name", on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="activities"
    )

    class Meta:
        """Meta definition for Activity."""

        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        """Unicode representation of Activities."""
        return self.title

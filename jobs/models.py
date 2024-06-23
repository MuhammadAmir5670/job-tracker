from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel

from .validators import valid_regex


class JobSource(models.Model):
    name = models.CharField(max_length=50)
    link_regex = models.CharField(max_length=500, blank=True, validators=[valid_regex])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("JobSource_detail", kwargs={"pk": self.pk})


class TechStack(TimeStampedModel):
    """Model definition for TechStack."""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Job(TimeStampedModel):
    """Model definition for Job."""

    class Status(models.TextChoices):
        WISHLIST = "WISHLIST", _("Wishlist")
        APPLIED = "APPLIED", _("Applied")
        INTERVIEW = "INTERVIEW", _("Interview")
        REJECTED = "REJECTED", _("Rejected")
        OFFER = "OFFER", _("Offer")
        DORMANT = "DORMANT", _("Dormant")
        FOLLOW_UP = "FOLLOW_UP", _("Follow Up")

    title = models.CharField(max_length=500)
    company = models.CharField(max_length=500)
    tech_stacks = models.ManyToManyField(TechStack)
    status = models.CharField(max_length=200, choices=Status.choices, default=Status.WISHLIST)
    link = models.TextField(validators=[URLValidator()])
    applied_at = models.DateTimeField(auto_now_add=True)
    job_source = models.ForeignKey(JobSource, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """Unicode representation of Job."""
        return self.title

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"pk": self.pk})

    def pretty_techstack(self):
        return ", ".join([tech_stack.name for tech_stack in self.tech_stacks.all()])

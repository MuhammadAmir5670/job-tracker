from django.db import models
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


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
    status = models.CharField(
        max_length=200, choices=Status.choices, default=Status.WISHLIST
    )
    link = models.TextField(validators=[URLValidator()])
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Unicode representation of Job."""
        return self.title

    def pretty_techstack(self):
        return ", ".join(self.tech_stacks.values_list("name", flat=True))

from django.conf import settings
from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel

from .validators import valid_regex


class JobSource(TimeStampedModel):
    name = models.CharField(max_length=50)
    link_regex = models.CharField(max_length=500, blank=True, validators=[valid_regex])

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("job_source_detail", kwargs={"pk": self.pk})


class TechStack(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class Job(TimeStampedModel):
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
    status = models.CharField(max_length=200, choices=Status.choices, default=Status.WISHLIST)
    link = models.TextField(validators=[URLValidator()])
    applied_at = models.DateTimeField(auto_now_add=True)
    job_source = models.ForeignKey(JobSource, related_name="jobs", on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="jobs", on_delete=models.PROTECT)
    tech_stacks = models.ManyToManyField(TechStack, related_name="jobs")

    def __str__(self):
        """Unicode representation of Job."""
        return self.title

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"pk": self.pk})

    def pretty_techstack(self):
        return ", ".join([tech_stack.name for tech_stack in self.tech_stacks.all()])


class Note(TimeStampedModel):
    content = models.TextField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("note_detail", kwargs={"pk": self.pk})

# Generated by Django 4.0.10 on 2024-06-09 14:35

from django.db import migrations


DEFAULT_ACTIVITIES = [
    "Email",
    "Meeting",
    "Phone Call",
    "Reach Out",
    "Get Reference",
    "Prep Cover Letter",
    "Apply",
    "Follow Up",
    "Send Availability",
    "Phone Screen",
    "Phone Interview",
    "Assignment",
    "On Site Interview",
    "Rejected",
    "Offer Received",
    "Prep Resume",
    "Decline Offer",
    "Accept Offer",
    "Other",
    "Prep for Interview",
    "Send Thank You",
    "Networking Event",
    "Application Withdrawn",
]


def add_activity_types(apps, schema_editor):
    ActivityType = apps.get_model("activities", "ActivityType")

    activities = [ActivityType(name=activity) for activity in DEFAULT_ACTIVITIES]
    ActivityType.objects.bulk_create(activities)

def remove_activity_types(apps, schema_editor):
    ActivityType = apps.get_model("activities", "ActivityType")

    ActivityType.objects.filter(name__in=DEFAULT_ACTIVITIES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_activity_types, remove_activity_types),
    ]

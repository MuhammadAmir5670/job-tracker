from django import forms

from activities.models import Activity, ActivityType


class ActivityForm(forms.ModelForm):
    """ActivityForm definition."""

    class Meta:
        model = Activity
        fields = ("title", "activity_type", "due_datetime", "completed", "note")


class ActivityTypeForm(forms.ModelForm):
    class Meta:
        model = ActivityType
        fields = "__all__"

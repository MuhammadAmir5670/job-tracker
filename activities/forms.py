from django import forms

from activities.models import Activity


class ActivityForm(forms.ModelForm):
    """ActivityForm definition."""

    class Meta:
        model = Activity
        fields = ("title", "activity_type", "due_datetime", "completed", "note")

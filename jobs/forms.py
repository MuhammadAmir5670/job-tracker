from django import forms

from django_tomselect.widgets import TomSelectMultipleWidget

from .models import Job


class TechStackWidget(TomSelectMultipleWidget):
    search_lookups = ["name__icontains"]


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = "__all__"
        widgets = {
            "tech_stacks": TechStackWidget,
            "link": forms.TextInput,
        }

import re

from django import forms
from django_tomselect.widgets import TomSelectMultipleWidget

from .models import Job, TechStack


class TechStackWidget(TomSelectMultipleWidget):
    search_lookups = ["name__icontains"]


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ("title", "company", "job_source", "link", "status", "tech_stacks", "description")
        widgets = {
            "tech_stacks": TechStackWidget,
            "link": forms.TextInput,
        }

    def clean(self):
        self._validate_job_source_link()

        return self.cleaned_data

    def _validate_job_source_link(self):
        job_link = self.cleaned_data.get("link")
        job_source = self.cleaned_data.get("job_source")

        if not job_source or not job_link:
            return

        if not re.match(job_source.link_regex, job_link):
            self.add_error("link", f"Not a valid URL for the selected Job Source: {job_source}")


class JobFilterForm(forms.Form):
    status_choices = [("", "------------")] + Job.Status.choices

    status = forms.ChoiceField(choices=status_choices, required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    tech_stacks = forms.ModelMultipleChoiceField(TechStack.objects, required=False, widget=TechStackWidget())

    def filter(self, queryset):
        if self.is_valid():
            status = self.cleaned_data["status"]
            start_date = self.cleaned_data["start_date"]
            end_date = self.cleaned_data["end_date"]
            tech_stacks = self.cleaned_data["tech_stacks"]

            if status:
                queryset = queryset.filter(status=status)
            if start_date:
                queryset = queryset.filter(applied_at__gte=start_date)
            if end_date:
                queryset = queryset.filter(applied_at_lte=end_date)
            if tech_stacks:
                queryset = queryset.filter(tech_stacks__in=tech_stacks)

        return queryset


class TechStackForm(forms.ModelForm):
    class Meta:
        model = TechStack
        fields = "__all__"

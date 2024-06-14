from django import forms
from django_tomselect.widgets import TomSelectMultipleWidget

from .models import Job, TechStack


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


class JobFilterForm(forms.Form):
    status_choices = [("", "------------")] + Job.Status.choices

    status = forms.ChoiceField(choices=status_choices, required=False)
    start_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    end_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    tech_stacks = forms.ModelMultipleChoiceField(
        TechStack.objects, required=False, widget=TechStackWidget()
    )

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
            if len(tech_stacks):
                queryset = queryset.filter(tech_stacks__in=tech_stacks)

        return queryset

from django.urls import reverse
from django.views import generic

from activities.models import Activity

from .forms import ActivityForm


class ActivityCreateView(generic.CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "activities/create_activity.html"

    def get_success_url(self) -> str:
        return reverse("job_detail", kwargs={"pk": self.kwargs["job_pk"]})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.job_id = self.kwargs["job_pk"]

        return super().form_valid(form)

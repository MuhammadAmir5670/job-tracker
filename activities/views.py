from django.urls import reverse
from django.views import generic

from core.viewmixins import PaginationMixin, SearchableMixin

from .forms import ActivityForm, ActivityTypeForm
from .models import Activity, ActivityType


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


class ActivityTypeListView(PaginationMixin, SearchableMixin, generic.ListView):
    model = ActivityType
    template_name = "activities/activity_type_list.html"
    context_object_name = "activity_type_list"
    search_lookups = ("name__icontains",)


class ActivityTypeBaseView(generic.FormView):
  model = ActivityType
  form_class = ActivityTypeForm

class ActivityTypeCreateView(ActivityTypeBaseView):
  template_name = "activities/activity_type_create.html"

class ActivityTypeUpdateView(ActivityTypeBaseView):
  template_name = "activities/activity_type_update.html"

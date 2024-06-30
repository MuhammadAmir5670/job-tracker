from django.urls import reverse
from django.views import generic

from core.viewmixins import FormActionMixin, PaginationMixin, SearchableMixin

from .forms import ActivityForm, ActivityTypeForm
from .models import Activity, ActivityType


class ActivityCreateView(FormActionMixin, generic.CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "activities/create_activity.html"
    success_message = "successfully logged job activity!"
    error_message = "error logging job activity!"

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
    form_class = ActivityTypeForm
    success_message = "successfully created activity!"
    error_message = "error creating activity!"


class ActivityTypeUpdateView(ActivityTypeBaseView):
    template_name = "activities/activity_type_update.html"
    form_class = ActivityTypeForm
    success_message = "successfully updated activity!"
    error_message = "error updating activity!"

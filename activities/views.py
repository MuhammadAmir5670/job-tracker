from django.urls import reverse_lazy
from django.views import generic

from core.mixins import AccessRequiredMixin
from core.viewmixins import FormActionMixin, PaginationMixin, SearchableMixin

from .forms import ActivityForm, ActivityTypeForm
from .models import Activity, ActivityType


class ActivityCreateView(AccessRequiredMixin, FormActionMixin, generic.CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "activities/create_activity.html"
    success_message = "successfully logged job activity!"
    error_message = "error logging job activity!"
    permission_required = "activities.log_activity"

    def get_success_url(self) -> str:
        return reverse_lazy("job_detail", kwargs={"pk": self.kwargs["job_pk"]})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.job_id = self.kwargs["job_pk"]

        return super().form_valid(form)


class ActivityTypeListView(AccessRequiredMixin, PaginationMixin, SearchableMixin, generic.ListView):
    model = ActivityType
    template_name = "activities/activity_type_list.html"
    context_object_name = "activity_type_list"
    search_lookups = ("name__icontains",)
    permission_required = "activities.view_activitytype"


class ActivityTypeDetailView(AccessRequiredMixin, generic.DetailView):
    model = ActivityType
    template_name = "activities/activity_type_detail.html"
    permission_required = "activities.view_activitytype"


class ActivityTypeCreateView(AccessRequiredMixin, generic.CreateView):
    model = ActivityType
    template_name = "activities/activity_type_create.html"
    form_class = ActivityTypeForm
    success_message = "successfully created activity!"
    error_message = "error creating activity!"
    permission_required = ("activities.add_activitytype", "activities.view_activitytype")


class ActivityTypeUpdateView(AccessRequiredMixin, generic.UpdateView):
    model = ActivityType
    template_name = "activities/activity_type_update.html"
    form_class = ActivityTypeForm
    success_message = "successfully updated activity!"
    error_message = "error updating activity!"
    permission_required = ("activities.view_activitytype", "activities.change_activitytype")


class ActivityTypeDeleteView(generic.DeleteView):
    model = ActivityType
    template_name = "activities/activity_type_delete.html"
    success_url = reverse_lazy("activity_type_list")
    permission_required = ("activities.view_activitytype", "activities.delete_activitytype")

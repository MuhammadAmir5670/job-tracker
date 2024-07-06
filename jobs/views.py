from django.urls import reverse_lazy
from django.views import generic

from activities.models import Activity
from core.viewmixins import FormActionMixin, PaginationMixin, SearchableMixin

from .forms import JobFilterForm, JobForm
from .models import Job, JobSource


class JobListView(PaginationMixin, SearchableMixin, generic.ListView):
    model = Job
    template_name = "jobs/jobs_list.html"
    context_object_name = "job_list"
    search_lookups = ("title__icontains", "company__icontains")

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("tech_stacks")
        filter_form = JobFilterForm(self.request.GET)

        if filter_form.is_valid():
            queryset = filter_form.filter(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["filter_form"] = JobFilterForm(self.request.GET)
        return context


class JobDetailView(generic.DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        activities = Activity.objects.select_related("activity_type", "creator")
        context["activities"] = activities.filter(job_id=self.object.pk)

        return context


class JobCreateView(FormActionMixin, generic.CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_create.html"
    success_message = "successfully created job!"
    error_message = "error creating job!"


class JobUpdateView(FormActionMixin, generic.UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_update.html"
    success_message = "successfully updated job!"
    error_message = "error updating job!"


class JobSourceListView(SearchableMixin, generic.ListView):
    model = JobSource
    search_lookups = ("name__icontains",)
    template_name = "job_sources/list.html"


class JobSourceDetailView(generic.DetailView):
    model = JobSource
    template_name = "job_sources/detail.html"


class JobSourceCreateView(generic.CreateView):
    model = JobSource
    template_name = "job_sources/create.html"
    fields = ["name", "link_regex"]


class JobSourceUpdateView(generic.UpdateView):
    model = JobSource
    template_name = "job_sources/update.html"
    fields = ["name", "link_regex"]


class JobSourceDeleteView(generic.DeleteView):
    model = JobSource
    template_name = "job_sources/delete.html"
    success_url = reverse_lazy("job_source_list")

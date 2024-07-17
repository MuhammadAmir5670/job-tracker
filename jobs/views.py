from django.urls import reverse_lazy
from django.views import generic

from activities.models import Activity
from core.mixins import AccessRequiredMixin
from core.viewmixins import FormActionMixin, PaginationMixin, SearchableMixin

from .forms import JobFilterForm, JobForm, TechStackForm
from .models import Job, JobSource, TechStack


class JobListView(AccessRequiredMixin, PaginationMixin, SearchableMixin, generic.ListView):
    model = Job
    template_name = "jobs/jobs_list.html"
    context_object_name = "job_list"
    search_lookups = ("title__icontains", "company__icontains")
    permission_required = "jobs.view_job"

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


class JobDetailView(AccessRequiredMixin, generic.DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"
    permission_required = "jobs.view_job"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        activities = Activity.objects.select_related("activity_type", "creator")
        context["activities"] = activities.filter(job_id=self.object.pk)

        return context


class JobCreateView(AccessRequiredMixin, FormActionMixin, generic.CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_create.html"
    success_message = "successfully created job!"
    error_message = "error creating job!"
    permission_required = ("jobs.add_job", "jobs.view_job")


class JobUpdateView(AccessRequiredMixin, FormActionMixin, generic.UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_update.html"
    success_message = "successfully updated job!"
    error_message = "error updating job!"
    permission_required = ("jobs.view_job", "jobs.change_job")


class JobDeleteView(AccessRequiredMixin, generic.DeleteView):
    model = Job
    template_name = "jobs/delete.html"
    success_url = reverse_lazy("job_list")
    permission_required = ("jobs.view_job", "jobs.delete_job")


class JobSourceListView(AccessRequiredMixin, SearchableMixin, generic.ListView):
    model = JobSource
    search_lookups = ("name__icontains",)
    template_name = "job_sources/list.html"
    permission_required = "jobs.view_jobsource"


class JobSourceDetailView(AccessRequiredMixin, generic.DetailView):
    model = JobSource
    template_name = "job_sources/detail.html"
    permission_required = "jobs.view_jobsource"


class JobSourceCreateView(AccessRequiredMixin, generic.CreateView):
    model = JobSource
    template_name = "job_sources/create.html"
    fields = ["name", "link_regex"]
    permission_required = ("jobs.view_jobsource", "jobs.add_jobsource")


class JobSourceUpdateView(AccessRequiredMixin, generic.UpdateView):
    model = JobSource
    template_name = "job_sources/update.html"
    fields = ["name", "link_regex"]
    permission_required = ("jobs.view_jobsource", "jobs.change_jobsource")


class JobSourceDeleteView(AccessRequiredMixin, generic.DeleteView):
    model = JobSource
    template_name = "job_sources/delete.html"
    success_url = reverse_lazy("job_source_list")
    permission_required = ("jobs.view_jobsource", "jobs.delete_jobsource")


class TechStackListView(AccessRequiredMixin, PaginationMixin, SearchableMixin, generic.ListView):
    model = TechStack
    template_name = "tech_stacks/list.html"
    context_object_name = "tech_stack_list"
    search_lookups = ("name__icontains",)
    permission_required = "jobs.view_techstack"


class TechStackBaseView(AccessRequiredMixin, FormActionMixin):
    model = TechStack
    form_class = TechStackForm
    success_url = reverse_lazy("tech_stack_list")


class TechStackCreateView(TechStackBaseView, generic.CreateView):
    template_name = "tech_stacks/create.html"
    success_message = "successfully created tech stack!"
    error_message = "error creating tech stack!"
    permission_required = ("jobs.view_techstack", "jobs.add_techstack")


class TechStackUpdateView(TechStackBaseView, generic.UpdateView):
    template_name = "tech_stacks/update.html"
    success_message = "successfully updated tech stack!"
    error_message = "error updating tech stack!"
    permission_required = ("jobs.view_techstack", "jobs.change_techstack")


class TechStackDeleteView(AccessRequiredMixin, generic.DeleteView):
    model = TechStack
    template_name = "tech_stacks/delete.html"
    success_url = reverse_lazy("tech_stack_list")
    permission_required = ("jobs.view_techstack", "jobs.delete_techstack")

from django.db.models import Q
from django.views import generic

from activities.models import Activity

from .forms import JobFilterForm, JobForm
from .models import Job


class JobsListView(generic.ListView):
    model = Job
    paginate_by = 10
    template_name = "jobs/jobs_list.html"
    context_object_name = "job_list"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        queryset = super().get_queryset().prefetch_related("tech_stacks")
        filter_form = JobFilterForm(self.request.GET)

        if query != "":
            queryset = queryset.filter(
                (Q(title__icontains=query) | Q(company__icontains=query))
            )

        if filter_form.is_valid():
            queryset = filter_form.filter(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        context["filter_form"] = JobFilterForm(self.request.GET)
        return context

    def paginate_queryset(self, queryset, page_size):
        paginator, page, object_list, has_other_pages = super().paginate_queryset(queryset, page_size)
        page.adjusted_elided_pages = paginator.get_elided_page_range(page.number)

        return (paginator, page, object_list, has_other_pages)


class JobDetailView(generic.DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        activities = Activity.objects.select_related("activity_type", "creator")
        context["activities"] = activities.filter(job_id=self.object.pk)

        return context


class JobCreateView(generic.CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_create.html"


class JobUpdateView(generic.UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_update.html"

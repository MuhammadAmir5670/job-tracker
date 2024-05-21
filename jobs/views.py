from django.views import generic

from jobs.models import Job


class JobsListView(generic.ListView):
    model = Job
    paginate_by = 10
    template_name = "jobs/jobs_list.html"
    context_object_name = "job_list"

    def paginate_queryset(self, queryset, page_size):
        paginator, page, object_list, has_other_pages = super().paginate_queryset(
            queryset, page_size
        )
        page.adjusted_elided_pages = paginator.get_elided_page_range(page.number)

        return (paginator, page, object_list, has_other_pages)


class JobDetailView(generic.DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"

from django.views import generic

from jobs.models import Job


class JobsListView(generic.ListView):
    model = Job
    template_name = "jobs/jobs_list.html"
    context_object_name = "job_list"

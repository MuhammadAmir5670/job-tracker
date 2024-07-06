from django.urls import path

from .views import JobCreateView, JobDetailView, JobListView, JobUpdateView

urlpatterns = [
    path("jobs/", JobListView.as_view(), name="jobs_list"),
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job_detail"),
    path("jobs/create/", JobCreateView.as_view(), name="job_create"),
    path("jobs/<int:pk>/update/", JobUpdateView.as_view(), name="job_update"),
]

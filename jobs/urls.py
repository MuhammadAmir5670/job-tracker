from django.urls import path

from .views import JobCreateView, JobDetailView, JobsListView, JobUpdateView

urlpatterns = [
    path("", JobsListView.as_view(), name="jobs_list"),
    path("<int:pk>/", JobDetailView.as_view(), name="job_detail"),
    path("create/", JobCreateView.as_view(), name="job_create"),
    path("<int:pk>/update/", JobUpdateView.as_view(), name="job_update"),
]

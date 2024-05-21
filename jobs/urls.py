from django.urls import path

from .views import JobCreateView, JobDetailView, JobsListView

urlpatterns = [
    path("", JobsListView.as_view(), name="jobs_list"),
    path("<int:pk>/", JobDetailView.as_view(), name="job_detail"),
    path("new/", JobCreateView.as_view(), name="job_create"),
]

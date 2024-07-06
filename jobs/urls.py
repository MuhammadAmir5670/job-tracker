from django.urls import path

from .views import (
    JobCreateView,
    JobDeleteView,
    JobDetailView,
    JobListView,
    JobSourceCreateView,
    JobSourceDeleteView,
    JobSourceDetailView,
    JobSourceListView,
    JobSourceUpdateView,
    JobUpdateView,
)

urlpatterns = [
    path("jobs/", JobListView.as_view(), name="job_list"),
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job_detail"),
    path("jobs/create/", JobCreateView.as_view(), name="job_create"),
    path("jobs/<int:pk>/update/", JobUpdateView.as_view(), name="job_update"),
    path("jobs/<int:pk>/delete/", JobDeleteView.as_view(), name="job_delete"),
    path("job_sources/", JobSourceListView.as_view(), name="job_source_list"),
    path("job_sources/<int:pk>/", JobSourceDetailView.as_view(), name="job_source_detail"),
    path("job_sources/create/", JobSourceCreateView.as_view(), name="job_source_create"),
    path("job_sources/<int:pk>/update/", JobSourceUpdateView.as_view(), name="job_source_update"),
    path("job_sources/<int:pk>/delete/", JobSourceDeleteView.as_view(), name="job_source_delete"),
]

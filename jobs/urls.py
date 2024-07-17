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
    TechStackListView,
    TechStackCreateView,
    TechStackUpdateView,
    TechStackDeleteView,
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
    path("tech_stacks/", TechStackListView.as_view(), name="tech_stack_list"),
    path("tech_stacks/create/", TechStackCreateView.as_view(), name="tech_stack_create"),
    path("tech_stacks/<int:pk>/update/", TechStackUpdateView.as_view(), name="tech_stack_update"),
    path("tech_stacks/<int:pk>/delete/", TechStackDeleteView.as_view(), name="tech_stack_delete"),
]

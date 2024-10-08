from django.urls import path

from .views import (
    ActivityCreateView,
    ActivityTypeCreateView,
    ActivityTypeDeleteView,
    ActivityTypeDetailView,
    ActivityTypeListView,
    ActivityTypeUpdateView,
)

urlpatterns = [
    path("<int:job_pk>", ActivityCreateView.as_view(), name="log_activity"),
    path("types/", ActivityTypeListView.as_view(), name="activity_type_list"),
    path("types/create", ActivityTypeCreateView.as_view(), name="activity_type_create"),
    path("types/<int:pk>", ActivityTypeDetailView.as_view(), name="activity_type_detail"),
    path(
        "types/<int:pk>/update",
        ActivityTypeUpdateView.as_view(),
        name="activity_type_update",
    ),
    path(
        "types/<int:pk>/delete",
        ActivityTypeDeleteView.as_view(),
        name="activity_type_delete",
    ),
]

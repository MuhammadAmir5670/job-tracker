from django.urls import path

from .views import ActivityCreateView

urlpatterns = [
    path("<int:job_pk>", ActivityCreateView.as_view(), name="activity_create"),
]

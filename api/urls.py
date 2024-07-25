from django.urls import include, path

from .jobs.urls import router as jobs_router

urlpatterns = [
    *jobs_router.urls,
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]

from django.urls import include, path

urlpatterns = [
    path("", include("api.jobs.urls")),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]

from django.urls import path

from core.views import RootView

urlpatterns = [path("", RootView.as_view(), name="root")]

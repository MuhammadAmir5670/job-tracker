from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .viewsets import JobNotesViewSet, JobViewSet, TechStackViewSet

router = DefaultRouter()

router.register("tech_stacks", TechStackViewSet, "tech_stack")
router.register("jobs", JobViewSet, "jobs")

jobs_router = NestedSimpleRouter(router, "jobs", lookup="job")
jobs_router.register("notes", JobNotesViewSet, "notes")


urlpatterns = [*router.urls, *jobs_router.urls]

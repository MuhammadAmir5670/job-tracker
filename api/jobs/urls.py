from rest_framework.routers import DefaultRouter

from .viewsets import JobViewSet, TechStackViewSet

router = DefaultRouter()

router.register("tech_stacks", TechStackViewSet, "tech_stack")
router.register("jobs", JobViewSet, "jobs")

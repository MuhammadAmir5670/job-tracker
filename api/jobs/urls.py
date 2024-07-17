from rest_framework.routers import DefaultRouter

from .views import TechStackViewSet

router = DefaultRouter()

router.register(r'tech_stacks', TechStackViewSet)

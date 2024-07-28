from rest_framework import filters, permissions, viewsets

from core.api.pagination import CustomCursorPagination
from core.api.permissions import CustomModelPermissions
from jobs.models import TechStack

from jobs.models import Job, TechStack

from .serializers import TechStackSerializer
from .serializers import JobSerializer, TechStackSerializer


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.all().order_by("-created_at")
    permission_classes = (permissions.DjangoModelPermissions,)


class TechStackViewSet(viewsets.ModelViewSet):
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer
    permission_classes = [CustomModelPermissions]
    pagination_class = CustomCursorPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

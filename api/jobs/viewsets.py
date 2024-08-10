from rest_framework import filters, viewsets

from core.api.pagination import CustomCursorPagination
from core.api.permissions import CustomModelPermissions
from jobs.models import Job, TechStack

from .serializers import JobSerializer, TechStackSerializer


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.order_by("-created_at")
    permission_classes = (CustomModelPermissions,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "company"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TechStackViewSet(viewsets.ModelViewSet):
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer
    permission_classes = [CustomModelPermissions]
    pagination_class = CustomCursorPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

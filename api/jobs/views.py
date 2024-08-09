from rest_framework import filters, viewsets

from core.api.pagination import CustomCursorPagination
from core.api.permissions import CustomModelPermissions
from jobs.models import TechStack

from .serializers import TechStackSerializer


class TechStackViewSet(viewsets.ModelViewSet):
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer
    permission_classes = [CustomModelPermissions]
    pagination_class = CustomCursorPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

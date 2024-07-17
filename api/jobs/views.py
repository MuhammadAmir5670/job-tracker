from rest_framework import viewsets, filters

from jobs.models import TechStack

from .serializers import TechStackSerializer
from .permissions import TechStackPermission
from .pagination import TechStackCursorPagination


class TechStackViewSet(viewsets.ModelViewSet):
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer
    permission_classes = [TechStackPermission]
    pagination_class = TechStackCursorPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

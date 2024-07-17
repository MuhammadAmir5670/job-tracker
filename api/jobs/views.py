from rest_framework import viewsets

from jobs.models import TechStack

from .serializers import TechStackSerializer
from .permissions import TechStackPermission


class TechStackViewSet(viewsets.ModelViewSet):
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer
    permission_classes = [TechStackPermission]

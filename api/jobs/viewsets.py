from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets

from core.api.pagination import CustomCursorPagination
from core.api.permissions import CustomModelPermissions
from jobs.models import Job, Note, TechStack

from .serializers import JobNotesSerializer, JobSerializer, TechStackSerializer


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.order_by("-created_at")
    permission_classes = (CustomModelPermissions,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "company"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class JobNotesViewSet(viewsets.ModelViewSet):
    serializer_class = JobNotesSerializer
    queryset = Note.objects.all().order_by("-created_at")
    permission_classes = (CustomModelPermissions,)

    def get_queryset(self):
        return super().get_queryset().filter(job_id=self.job)

    def perform_create(self, serializer):
        serializer.save(job_id=self.job)

    @property
    def job(self):
        return get_object_or_404(Job, pk=self.kwargs["job_pk"])


class TechStackViewSet(viewsets.ModelViewSet):
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer
    permission_classes = [CustomModelPermissions]
    pagination_class = CustomCursorPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

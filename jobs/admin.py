from django.contrib import admin

from .forms import JobForm
from .models import Job, JobSource, TechStack


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    form = JobForm
    list_display = (
        "title",
        "company",
        "status",
    )


admin.site.register([TechStack, JobSource])

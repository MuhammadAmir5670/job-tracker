from django.contrib import admin

from .models import TechStack, Job

admin.site.register(Job, TechStack)

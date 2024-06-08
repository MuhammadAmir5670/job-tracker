from django.contrib import admin

from .models import Job, TechStack

admin.site.register([Job, TechStack])

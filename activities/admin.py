from django.contrib import admin

from .models import Activity, ActivityType

admin.site.register([ActivityType, Activity])

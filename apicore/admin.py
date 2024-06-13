# scraper/admin.py
from django.contrib import admin
from .models import Job, Task

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'created_at', 'status')
    search_fields = ('job_id', 'status')
    list_filter = ('status', 'created_at')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('job', 'coin', 'status', 'created_at')
    search_fields = ('coin', 'status')
    list_filter = ('status', 'created_at')

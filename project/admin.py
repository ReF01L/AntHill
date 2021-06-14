from django.contrib import admin
from .models import Project, Issue, Sprint, LoggedTime


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    filter_horizontal = ['users']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['project',
                    'verifier',
                    'executor',
                    'priority',
                    'status',
                    'type',
                    'summary',
                    'description',
                    'environment',
                    'ETA',
                    'percent',
                    'created',
                    'updated',
                    'original_estimate']


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'due_date']


@admin.register(LoggedTime)
class LoggedTimeAdmin(admin.ModelAdmin):
    list_display = ['issue', 'date', 'hours_count', 'description']

from django.contrib import admin
from .models import Project, Issue, Sprint


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    filter_horizontal = ['users']


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


class SprintAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'due_date']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Sprint, SprintAdmin)

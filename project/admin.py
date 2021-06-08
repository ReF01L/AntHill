from django.contrib import admin
from .models import Project, Issue, IssuePriority, IssueResolution


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    filter_horizontal = ['users']


class IssueAdmin(admin.ModelAdmin):
    list_display = ['project',
                    'verifier',
                    'executor',
                    'resolution',
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
                    'resolution_dated']
    filter_horizontal = ['watchers']


class IssuePriorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


class IssueResolutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(IssuePriority, IssuePriorityAdmin)
admin.site.register(IssueResolution, IssueResolutionAdmin)

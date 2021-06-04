from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from pytz import unicode

from AntHill import settings
from account.models import Profile
from project.models import Project


def projects(request):
    return render(request, 'project/projects.html')


def command(request, project):
    var = Project.objects.create(name='commandModelName')
    print(var)
    print(project)
    # var.delete()
    request.session[settings.KEY] = 'css'
    request.session.save()
    return redirect('account:profile')


@require_GET
def recent_project(request):
    var = Profile.objects.get(user=request.user)
    project_set = var.project_set.all()
    return render(request, 'project/projects.html', {'project_names': [x.name for x in project_set]})

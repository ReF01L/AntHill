from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from AntHill import settings
from account.models import Profile
from project.models import Project


@login_required
def projects(request):
    user = Profile.objects.get(user=request.user)
    _projects = user.project_set.all()
    if _projects:
        return render(request, 'project/project_exists.html', {
            'projects': user.project_set.all()
        })
    return render(request, 'project/project_not_exists.html')


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


def create_project(request):
    return redirect('project:projects')


def join_project(request):
    return redirect('project:projects')

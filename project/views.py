from django.shortcuts import render, redirect

from AntHill import settings
from project.models import Project


def project(request):
    return render(request, 'project/project.html')


def projects(request):
    return render(request, 'project/user_projects.html')


def command(request, project):
    var = Project.objects.create(name='commandModelName')
    print(var)
    print(project)
    # var.delete()
    request.session[settings.KEY] = 'css'
    request.session.save()
    return redirect('account:profile')

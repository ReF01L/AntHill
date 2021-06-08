from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from pytz import unicode

from AntHill import settings
from project.forms import ChooseProjectForm
from account.models import Profile
from project.models import Project


def project(request):
    return render(request, 'project/project.html')


def projects(request):
    return render(request, 'project/user_projects.html')


def create_project(request):
    return render(request, 'project/create_project.html')


def board(request):
    return render(request, 'project/board.html')


def create_issue(request):
    if request.method == 'POST':
        form = ChooseProjectForm(request.POST)
        form.is_valid()

    return render(request, 'project/create_issue.html', {
        'form': ChooseProjectForm()
    })


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

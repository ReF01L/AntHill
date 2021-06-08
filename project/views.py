from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

from AntHill import settings
from account.models import Profile
from project.forms import CreateProjectForm
from project.models import Project


@login_required(login_url='/account/login/')
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


@login_required(login_url='/account/login/')
def create_project(request):
    form = CreateProjectForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = Profile.objects.get(user=request.user)
            proj = Project.objects.create(name=cd.get('name'), description=cd.get('description'))
            for x in cd.get('users'):
                proj.users.add(x)
            return redirect('project:board')

    return render(request, 'project/create.html', {'form': form})


@login_required(login_url='/account/login/')
def join_project(request):
    return redirect('project:projects')


@login_required(login_url='/account/login/')
def board(request):
    return render(request, 'project/board.html')

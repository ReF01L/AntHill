from random import choice
from string import ascii_letters

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
    all_u = Project.objects.filter(users__in=[user])

    if all_u:
        recents = all_u[:6]
        recents += list([x for x in range(6 - len(recents))])
        return render(request, 'project/project_exists.html', {
            'recents': recents,
            'all': all_u
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
            proj = Project.objects.create(name=cd.get('name'), description=cd.get('description'), key=cd['link'])
            proj.users.add(user)
            return redirect('project:board')

    return render(request, 'project/create.html', {'form': form})


@login_required(login_url='/account/login/')
def join_project(request):
    key = request.POST.get('key') or request.GET.get('key') or 0
    if key != 0:
        user = Profile.objects.get(user=request.user)
        try:
            proj = Project.objects.get(key=key)
            proj.users.add(user)
            return render(request, 'project/join_success.html')
        except Project.DoesNotExist:
            pass

    return render(request, 'project/join_fail.html')


@login_required(login_url='/account/login/')
def board(request):
    return render(request, 'project/board.html')

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from account.models import Profile
from project import constants
from project.forms import CreateProjectForm, CreateIssueForm, CreateLogForm
from project.models import Project, Issue, Sprint


@login_required(login_url='/account/login/')
def projects(request):
    user = Profile.objects.get(user=request.user)
    all_u = Project.objects.filter(users__in=[user])

    if all_u:
        recent = all_u[:6]
        empty = range(6 - len(recent))
        _all = [{
            'name': project.name,
            'username': project.users.all()[0].user.username,
            'key': project.slug
        } for project in all_u]
        return render(request, 'project/project_exists.html', {
            'recent': recent,
            'all': _all,
            'empty': empty
        })
    return render(request, 'project/project_not_exists.html')


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
            proj = Project.objects.create(name=cd.get('name'), description=cd.get('description'),
                                          slug=cd['link'].split('/')[-1])
            proj.users.add(user)
            return redirect('project:board', 'kPaQDGUdPZ')

    return render(request, 'project/create.html', {'form': form})


@login_required(login_url='/account/login/')
def join_project(request):
    key = request.POST.get('key') or request.GET.get('key') or 0
    if key != 0:
        user = Profile.objects.get(user=request.user)
        proj = Project.objects.filter(slug=key)
        proj.users.add(user)
        return render(request, 'project/join_success.html')

    return render(request, 'project/join_fail.html')


@login_required(login_url='/account/login/')
def board(request, slug):
    project = Project.objects.get(slug=slug)
    tickets = {
        'waiting': [x for x in project.issue_set.filter(status=constants.Statuses.WAITING)],
        'progress': [x for x in project.issue_set.filter(status=constants.Statuses.PROGRESS)],
        'complete': [x for x in project.issue_set.filter(status=constants.Statuses.COMPLETE)]
    }
    return render(request, 'project/board.html', {
        'waiting': tickets['waiting'],
        'progress': tickets['progress'],
        'complete': tickets['complete'],
        'project': project
    })


@login_required(login_url='/account/login/')
def create_issue(request, slug):
    project = Project.objects.get(slug=slug)
    if request.method == 'POST':
        form = CreateIssueForm(request.POST)
        if form.valid():
            cd = form.cleaned_data
            issue = Issue.objects.create(
                status=cd.get('status'),
                type=cd.get('type'),
                priority=cd.get('priority'),
                summary=cd.get('summary'),
                description=cd.get('description'),
                percent=cd.get('percent'),
                environment=cd.get('environment'),
                ETA=cd.get('ETA'),
                project=project,
                slug=cd.get(slug)
            )
    else:
        form = CreateIssueForm()
        form.fields['verifier'].choices = [(x.user.username, x.user.username) for x in project.users.all()]

        form.fields['sprint'].choices = [('', '')]
        if project.sprint is not None:
            form.fields['sprint'].choices += [(project.sprint.name, project.sprint.name)]
        form.fields['executor'].choices = [(x.user.username, x.user.username) for x in project.users.all()]
    return render(request, 'project/create_issue.html', {
        'form': form
    })


def issues(request, slug):
    return HttpResponse('Issues')


def roadmap(request, slug):
    return HttpResponse('RoadMap')


def log(request, slug):
    form = CreateLogForm()
    form.fields['issue'].choices = [(x.summary, x.summary) for x in Issue.objects.all()]

    return render(request, 'project/log.html', {
        'project': Project.objects.get(slug=slug),
        'form': form,
    })

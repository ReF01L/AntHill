from random import choice
from string import ascii_letters

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from account.models import Profile
from project import constants
from project.forms import CreateProjectForm, CreateIssueForm
from project.models import Project, Issue, Sprint, LoggedTime
from project.forms import CreateProjectForm, CreateIssueForm, CreateSprintForm
from project.models import Project, Issue, Sprint
from project.forms import CreateProjectForm, IssueHeroForm, IssueInfoForm
from project.models import Project, Issue
from project.forms import CreateProjectForm, CreateIssueForm, CreateLogForm
from project.models import Project, Issue, Sprint
from . import constants
from .forms import CreateProjectForm, CreateIssueForm
from .models import Project, Issue, Sprint
from .forms import CreateProjectForm, IssueHeroForm, IssueInfoForm
from .models import Project, Issue
from .utils import parser_estimate, parser_to_str, user_in_project


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
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = Profile.objects.get(user=request.user)
            proj = Project.objects.create(name=cd.get('name'), description=cd.get('description'),
                                          slug=cd['link'].split('/')[-1])
            proj.users.add(user)
            return redirect('project:board', cd['link'].split('/')[-1])
    else:
        form = CreateProjectForm(
            initial={'link': 'http://localhost:8000/project/' + ''.join(choice(ascii_letters) for _ in range(10))})
    return render(request, 'project/create.html', {'form': form})


@login_required(login_url='/account/login/')
def join_project(request):
    slug = request.POST.get('slug')
    if slug:
        slug = slug.split('/')[-1]
        try:
            project = Project.objects.get(slug=slug)
            user = Profile.objects.get(user=request.user)
            if user in project.users.all():
                return redirect('project:board', slug=slug)
            project.users.add(user)
            project.save()
        except Project.DoesNotExist:
            return render(request, 'project/join_fail.html')
        return redirect('project:board', slug=slug)

    return render(request, 'project/join_fail.html')


@login_required(login_url='/account/login/')
def board(request, slug):
    project = Project.objects.get(slug=slug)
    if user_in_project(request, project):
        return redirect('project:join')
    if project.sprint:
        tickets = {
            'waiting': [x for x in project.sprint.issue_set.filter(status=constants.Statuses.WAITING)],
            'progress': [x for x in project.sprint.issue_set.filter(status=constants.Statuses.PROGRESS)],
            'complete': [x for x in project.sprint.issue_set.filter(status=constants.Statuses.COMPLETE)]
        }
        [setattr(x, 'shortname', x.verifier.user.last_name[0] + x.verifier.user.first_name[0]) for x in (
                tickets['waiting'] + tickets['progress'] + tickets['complete']
        )]
        users = [x.user.last_name[0] + x.user.first_name[0] for x in Project.objects.get(slug=slug).users.all()]
        return render(request, 'project/board.html', {
            'waiting': tickets['waiting'],
            'progress': tickets['progress'],
            'complete': tickets['complete'],
            'project': project,
            'sprint': project.sprint,
            'shortname': users
        })
    else:
        return render(request, 'project/board.html', {
            'project': project,
            'sprint': None,
        })


@login_required(login_url='/account/login/')
def create_issue(request, slug):
    project = Project.objects.get(slug=slug)
    if user_in_project(request, project):
        return redirect('project:join')
    if request.method == 'POST':
        form = CreateIssueForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Issue.objects.create(
                status=cd.get('status'),
                type=cd.get('type'),
                priority=cd.get('priority'),
                summary=cd.get('summary'),
                description=cd.get('description'),
                percent=cd.get('percent'),
                environment=cd.get('environment'),
                ETA=cd.get('ETA'),
                project=project,
                slug=cd.get('slug'),
                sprint=cd.get('sprint'),
                verifier=cd.get('verifier'),
                executor=cd.get('executor'),
                original_estimate=parser_estimate(cd.get('original_estimate'))
            )
            return redirect('project:issue', project_slug=slug, issue_slug=cd.get('slug'))
    else:
        form = CreateIssueForm(initial={'slug': ''.join(choice(ascii_letters) for _ in range(10))})
    form.fields['sprint'].queryset = Sprint.objects.filter(name=project.sprint.name)
    return render(request, 'project/create_issue.html', {
        'form': form,
        'project': project,
    })


@login_required(login_url='/account/login/')
def issues(request, slug):
    project = Project.objects.get(slug=slug)
    if user_in_project(request, project):
        return redirect('project:join')
    _issues = project.issue_set.all()
    status = request.GET.get('status') == 'True'
    executor = request.GET.get('executor') == 'True'
    if status:
        _issues = _issues.filter(status__in=[constants.Statuses.WAITING, constants.Statuses.PROGRESS])
    if executor:
        _issues = _issues.filter(executor=Profile.objects.get(user=request.user))
    return render(request, 'project/all_issues.html', {
        'project': project,
        'issues': _issues,
        'status': status,
        'executor': executor,
    })


@login_required(login_url='/account/login/')
def log(request, slug):
    project = Project.objects.get(slug=slug)
    if user_in_project(request, project):
        return redirect('project:join')
    form = CreateLogForm(request.POST or None)
    form.fields['issue'].queryset = Issue.objects.filter(project=project)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            LoggedTime.objects.create(
                issue=cd['issue'],
                hours_count=parser_estimate(cd.get('hours_count')),
                description=cd['description']
            )
            return redirect('project:issue', project_slug=project.slug, issue_slug=cd['issue'].slug)

    return render(request, 'project/log.html', {
        'project': Project.objects.get(slug=slug),
        'form': form,
    })


@login_required(login_url='/account/login/')
def issue(request, project_slug, issue_slug):
    project = Project.objects.get(slug=project_slug)
    if user_in_project(request, project):
        return redirect('project:join')
    _issue = Issue.objects.get(slug=issue_slug)
    logged_time = sum((x.hours_count for x in LoggedTime.objects.filter(issue=_issue)))
    original_estimate = parser_to_str(_issue.original_estimate)
    remaining_estimate = parser_to_str(_issue.original_estimate - logged_time)
    if remaining_estimate[0] == '-':
        remaining_estimate = 0
    if request.method == 'POST':
        form = IssueHeroForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            _issue.description = cd['description']
            _issue.environment = cd['environment']
            _issue.status = cd['status']
            _issue.percent = cd['percent']
            _issue.save()

    return render(request, 'project/issue.html', {
        'issue': _issue,
        'project': project,
        'hero_form': IssueHeroForm(initial={
            'description': _issue.description,
            'environment': _issue.environment,
            'status': _issue.status,
            'percent': _issue.percent,
        }),
        'info_form': IssueInfoForm(initial={
            'project': project.name,
            'verifier': _issue.verifier.user.username,
            'executor': _issue.executor.user.username,
            'priority': _issue.priority,
            'original_estimate': original_estimate,
            'remaining_estimate': remaining_estimate,
        }),
    })


@login_required(login_url='/account/login/')
def create_sprint(request, slug):
    project = Project.objects.get(slug=slug)
    if user_in_project(request, project):
        return redirect('project:join')
    form = CreateSprintForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            sprint = Sprint.objects.create(
                name=cd.get('name'),
                due_date=cd.get('due_date'),
            )
            project.sprint = sprint
            project.save()
            return redirect('project:board', slug)
    return render(request, 'project/create_sprint.html', {
        'form': form,
        'project': project,
    })


@login_required(login_url='/account/login/')
def edit_sprint(request, slug):
    project = Project.objects.get(slug=slug)
    if user_in_project(request, project):
        return redirect('project:join')
    sprint = project.sprint
    if request.method == "POST":
        form = CreateSprintForm(data=request.POST, instance=sprint)
        if form.is_valid():
            form.save()
            return redirect('project:board', slug=slug)
    else:
        form = CreateSprintForm(instance=sprint)
    return render(request, "project/edit_sprint.html", {'form': form, 'project': project})


@login_required(login_url='/account/login/')
def delete_sprint(request, slug):
    project = Project.objects.get(slug=slug)
    if user_in_project(request, project):
        return redirect('project:join')
    sprint = project.sprint
    project.sprint = None
    project.save()
    sprint.delete()
    return redirect('project:issues', slug=slug)


@login_required(login_url='/account/login/')
def delete_issue(request, project_slug, issue_slug):
    if user_in_project(request, Project.objects.get(slug=project_slug)):
        return redirect('project:join')
    _issue = Issue.objects.get(slug=issue_slug)
    _issue.delete()
    return redirect('project:issues', slug=project_slug)

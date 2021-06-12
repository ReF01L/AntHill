from random import choice
from string import ascii_letters

from django import forms
from django.forms import CheckboxSelectMultiple

from account.models import Profile
from .models import Project

from project.models import Project, Issue


class JoinProjectForm(forms.ModelForm):
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(),
        widget=forms.RadioSelect
    )

    class Meta:
        model = Project
        fields = ('projects',)


class CreateProjectForm(forms.ModelForm):
    description = forms.CharField(label='Description', label_suffix='', widget=forms.Textarea(
        attrs={
            'class': 'create_project_form-field'
        }
    ))
    name = forms.CharField(label='Name of the project', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'create_project_form-field'
        }
    ))
    link = forms.CharField(label='Link for the join to this project', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'create_project_form-field',
            'readonly': True,
            'value': 'http://localhost:8000/project/' + ''.join(choice(ascii_letters) for _ in range(10))
        }
    ))

    class Meta:
        model = Project
        fields = ('name', 'description')


class ChooseProjectForm(forms.ModelForm):
    error_css_class = 'error'
    # PROJECTS = ((x.name, x.name) for x in Project.objects.all())
    # EXECUTORS = ((x.executor.user.username, x.executor.user.username) for x in Issue.objects.all())
    TASK_TYPE = (('Epic', 'Epic'), ('notEpic', 'notEpic'))

    projects = forms.ChoiceField(label='Project', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ))
    task_type = forms.ChoiceField(label='Task Type', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ), choices=TASK_TYPE)
    issue = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'issue_body_form-name'
        }
    ))
    desc = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'issue_body_form-description'
        }
    ))
    executor = forms.ChoiceField(label='Executor', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ))
    sprint = forms.ChoiceField(label='Sprint', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ))
    story_point_estimate = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'issue_body_form-name'
        }
    ))
    author = forms.CharField(label='Author', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ))

    class Meta:
        model = Issue
        fields = ()


class IssueHeroForm(forms.ModelForm):
    description = forms.CharField(label='Description', label_suffix='', widget=forms.Textarea(
        attrs={
            'class': 'issue_body-hero_form-field'
        }
    ))
    environment = forms.CharField(label='Environment', label_suffix='', widget=forms.Textarea(
        attrs={
            'class': 'issue_body-hero_form-field'
        }
    ))

    class Meta:
        model = Issue
        fields = ('description', 'environment')


class IssueInfoForm(forms.ModelForm):
    project = forms.CharField(label='project', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'issue_body-info_form-field',
            'readonly': True
        }
    ))
    verifier = forms.CharField(label='verifier', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'issue_body-info_form-field',
            'readonly': True
        }
    ))
    executor = forms.CharField(label='executor', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'issue_body-info_form-field',
            'readonly': True
        }
    ))
    status = forms.CharField(label='status', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'issue_body-info_form-field',
            'readonly': True
        }
    ))
    priority = forms.CharField(label='priority', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'issue_body-info_form-field',
            'readonly': True
        }
    ))
    percent = forms.CharField(label='percent', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'issue_body-info_form-field',
            'readonly': True
        }
    ))
    original_estimate = forms.CharField(label='original estimate', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'issue_body-info_form-field',
            'readonly': True
        }
    ))
    remaining_estimate = forms.CharField(label='remaining estimate', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'issue_body-info_form-field',
            'readonly': True
        }
    ))

    class Meta:
        model = Issue
        fields = (
            'project',
            'verifier',
            'executor',
            'status',
            'priority',
            'percent',
        )

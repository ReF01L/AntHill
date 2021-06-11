from random import choice
from string import ascii_letters

from django import forms
from django.forms import CheckboxSelectMultiple

from account.models import Profile
from . import constants
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

    projects = forms.ChoiceField(label='Project', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ))
    task_type = forms.ChoiceField(label='Task Type', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ), choices=constants.Types.choices)
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


class CreateIssueForm(forms.ModelForm):
    sprint = forms.ChoiceField(label='Sprint', label_suffix='', widget=forms.Select)
    verifier = forms.ChoiceField(label='Verifiers', label_suffix='', widget=forms.Select)
    executor = forms.ChoiceField(label='Executor', label_suffix='', widget=forms.Select)
    status = forms.ChoiceField(label='Status', label_suffix='', widget=forms.Select,
                               choices=constants.Statuses.choices, initial=constants.Statuses.WAITING)
    type = forms.ChoiceField(label='Type', label_suffix='', widget=forms.Select, choices=constants.Types.choices)
    priority = forms.ChoiceField(label='Priority', label_suffix='', widget=forms.Select,
                                 choices=constants.Priority.choices)
    summary = forms.CharField(label='Name Issue', label_suffix='', max_length=100)
    description = forms.CharField(label='Description', label_suffix='', max_length=300)
    environment = forms.CharField(label='Environment', label_suffix='')
    ETA = forms.DateField(label='ETA', label_suffix='', widget=forms.DateInput(format=('%d-%m-%Y'),
                                                                               attrs={'class': 'myDateClass',
                                                                                      'placeholder': 'Select a date'}))
    percent = forms.IntegerField(label='Story point estimate', label_suffix='', widget=forms.NumberInput)
    slug = forms.SlugField(label='Issue Key', label_suffix='', widget=forms.TextInput(attrs={
        'readonly': True,
        'value': ''.join(choice(ascii_letters) for _ in range(10))
    }))

    class Meta:
        model = Issue
        fields = ('sprint', 'verifier',
                  'executor', 'status', 'type',
                  'priority', 'summary', 'description',
                  'environment', 'ETA', 'percent', 'slug',)

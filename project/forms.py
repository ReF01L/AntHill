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
    # TASK_TYPE = (('Epic', 'Epic'), ('notEpic', 'notEpic'))
    # AUTHOR = ((x.verifier.user.username, x.verifier.user.username) for x in Issue.objects.all())
    # PARENT_ISSUE = ((x.objects.name, x.objects.name) for x in Issue.objects.all())

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
    author = forms.ChoiceField(label='Author', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ))
    parent_issue = forms.ChoiceField(label='Parent issue', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ), choices=(('Parent1', 'Parent1'), ('Parent2', 'Parent2')))  # todo fix parent_issue

    class Meta:
        model = Issue
        fields = ()


class CreateIssueForm(forms.ModelForm):
    summary = forms.CharField(label='Name Issue', label_suffix='', max_length=100)
    type = forms.ChoiceField(label='Type', label_suffix='', widget=forms.Select, choices=constants.Types.choices)
    description = forms.CharField(label='Description', label_suffix='', max_length=300, widget=forms.Textarea(
        attrs={
            'cols': 80,
        }
    ))
    executor = forms.ChoiceField(label='Executor', label_suffix='', widget=forms.Select)
    sprint = forms.ChoiceField(label='Sprint', label_suffix='', widget=forms.Select)
    percent = forms.IntegerField(label='Story point estimate', label_suffix='', widget=forms.NumberInput)
    verifier = forms.ChoiceField(label='Verifiers', label_suffix='', widget=forms.Select)
    ETA = forms.DateField(label='ETA', label_suffix='', widget=forms.DateInput(format=('%d-%m-%Y'),
                                                                               attrs={'class': 'myDateClass',
                                                                                      'placeholder': 'Select a date'}))
    priority = forms.ChoiceField(label='Priority', label_suffix='', widget=forms.Select,
                                 choices=constants.Priority.choices)
    status = forms.ChoiceField(label='Status', label_suffix='', widget=forms.Select,
                               choices=constants.Statuses.choices, initial=constants.Statuses.WAITING)
    environment = forms.CharField(label='Environment', label_suffix='', widget=forms.Textarea(
        attrs={
            'cols': 80,
        }
    ))
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


class CreateLogForm(forms.ModelForm):
    issue = forms.ChoiceField(label='Issue', label_suffix='', widget=forms.Select())
    time_spend = forms.CharField(label='Time Spend', label_suffix='', max_length=100, widget=forms.Textarea(
        attrs={
            'cols': 80,
            'rows': 1,
        }
    ))
    desc = forms.CharField(label='Description', label_suffix='', widget=forms.Textarea(
        attrs={
            'cols': 80,
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

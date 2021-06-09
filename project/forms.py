from django import forms

from account.models import Profile
from .models import Project

from project.models import Project, Issue


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description',)


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

    def clean_issue(self):
        issue = self.cleaned_data.get('issue')
        print(issue)
        return self.cleaned_data.get('projects')
        model = Project
        fields = ('name', 'description', 'users')

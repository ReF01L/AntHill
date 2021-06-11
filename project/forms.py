from django import forms

from project.models import Project, Issue


class ChooseProjectForm(forms.ModelForm):
    error_css_class = 'error'
    PROJECTS = ((x.name, x.name) for x in Project.objects.all())
    EXECUTORS = ((x.executor.user.username, x.executor.user.username) for x in Issue.objects.all())
    TASK_TYPE = (('Epic', 'Epic'), ('notEpic', 'notEpic'))
    AUTHOR = ((x.verifier.user.username, x.verifier.user.username) for x in Issue.objects.all())
    # PARENT_ISSUE = ((x.objects.name, x.objects.name) for x in Issue.objects.all())

    projects = forms.ChoiceField(label='Project', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ), choices=PROJECTS)
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
    ), choices=EXECUTORS)
    sprint = forms.ChoiceField(label='Sprint', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ), choices=(('Sprint1', 'Sprint1'), ('Sprint2', 'Sprint2')))  # todo fix sprint
    story_point_estimate = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'issue_body_form-name'
        }
    ))
    author = forms.ChoiceField(label='Author', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ), choices=AUTHOR)
    parent_issue = forms.ChoiceField(label='Parent issue', label_suffix='', widget=forms.Select(
        attrs={
            'class': 'issue_body_form-field'
        }
    ), choices=(('Parent1', 'Parent1'), ('Parent2', 'Parent2')))  # todo fix parent_issue

    class Meta:
        model = Issue
        fields = ()

    def clean_issue(self):
        issue = self.cleaned_data.get('issue')
        print(issue)
        return self.cleaned_data.get('projects')

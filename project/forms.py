from django import forms

from account.models import Profile
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('users', 'name', 'description')


class CreateProjectForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Project
        fields = ('name', 'description', 'users')

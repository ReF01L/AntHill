from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.models import Profile


class IssueResolution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)


class IssuePriority(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(null=True, blank=True, upload_to='project/%Y/%m/%d')


class Project(models.Model):
    users = models.ManyToManyField(to=Profile)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    key = models.CharField(max_length=20, null=True, blank=True)


class LoggedTime(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    hours_count = models.TimeField()
    description = models.TextField()


class Issue(models.Model):
    watchers = models.ManyToManyField(to=Profile)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    verifier = models.ForeignKey(to=Profile, on_delete=models.DO_NOTHING, related_name='verifier')
    executor = models.ForeignKey(to=Profile, on_delete=models.DO_NOTHING, related_name='executor')
    resolution = models.ForeignKey(to=IssueResolution, on_delete=models.CASCADE)
    priority = models.ForeignKey(to=IssuePriority, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    summary = models.TextField()
    description = models.TextField(null=True, blank=True)
    environment = models.TextField(null=True, blank=True)
    ETA = models.DateTimeField(auto_now_add=False, auto_now=False)
    percent = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    resolution_dated = models.DateTimeField(auto_now_add=False, auto_now=False)

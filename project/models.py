from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.models import Profile
from project import constants


class Sprint(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return self.name


class Project(models.Model):
    users = models.ManyToManyField(to=Profile)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=20)
    sprint = models.OneToOneField(to=Sprint, on_delete=models.SET_NULL, null=True, blank=True)


class Issue(models.Model):
    sprint = models.ForeignKey(to=Sprint, on_delete=models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    verifier = models.ForeignKey(to=Profile, on_delete=models.DO_NOTHING, related_name='verifier')
    executor = models.ForeignKey(to=Profile, on_delete=models.DO_NOTHING, related_name='executor')
    status = models.CharField(max_length=20, choices=constants.Statuses.choices)
    type = models.CharField(max_length=20, choices=constants.Types.choices)
    priority = models.CharField(max_length=20, choices=constants.Priority.choices)
    summary = models.TextField(max_length=100)  # name
    description = models.TextField(null=True, blank=True)
    environment = models.TextField(null=True, blank=True)  # status notes
    ETA = models.DateField(auto_now_add=False, auto_now=False)
    percent = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=20)
    original_estimate = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.summary


class LoggedTime(models.Model):
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    hours_count = models.PositiveIntegerField()
    description = models.TextField()




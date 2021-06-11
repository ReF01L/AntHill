from django.db import models
from django.utils.translation import gettext_lazy as _


class Types(models.TextChoices):
    TASK = 'Task', _('Task')
    BUG = 'Bug', _('Bug')
    EPIC = 'Epic', _('Epic')
    STORY = 'Story', _('Story')


class Statuses(models.TextChoices):
    WAITING = 'Waiting', _('Waiting')
    PROGRESS = 'Progress', _('Progress')
    COMPLETE = 'Complete', _('Complete')


class Priority(models.TextChoices):
    HIGHEST = 'Highest', _('Highest')
    HIGH = 'High', _('High')
    MEDIUM = 'Medium', _('Medium')
    LOW = 'Low', _('Low')

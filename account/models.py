from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=4, default='0000')

    def __str__(self):
        return self.user.username

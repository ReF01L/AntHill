from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)  # TODO:  default image
    phone = models.TextField(null=True, blank=True)
    notification = models.IntegerField(null=True, blank=True)  # TODO: need?
    code = models.CharField(max_length=4, default='0000')

    def __str__(self):
        return self.user.username

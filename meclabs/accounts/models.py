from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
    User,
    models.SET_NULL,
    blank=True,
    null=True,
)
    FirstName = models.CharField(max_length=100, default='')
    LastName = models.CharField(max_length=100, default='')
    PhoneNumber = models.CharField(max_length=100, default='')
    Email = models.CharField(max_length=200,default='')

    def __str__(self):
        return '%s' % (self.user)

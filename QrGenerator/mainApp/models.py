from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        primary_key=True,
    )
class project(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=100)
    collaborator = models.ManyToManyField(profile)


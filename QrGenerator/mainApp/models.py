from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        primary_key=True,
    )
class Project(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    collaborators = models.ManyToManyField(Profile)
    qr_number = models.SmallIntegerField(default=0)


class ProjectProfile(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Qr(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')


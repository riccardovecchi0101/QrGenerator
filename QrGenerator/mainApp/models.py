from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        primary_key=True,
    )
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    collaborators = models.ManyToManyField(Profile)
    qr_number = models.SmallIntegerField(default=0)
    total_times_scanned = models.IntegerField(default = 0)


class ProjectProfile(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Qr(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    times_scanned = models.IntegerField(default=0)
    image = ResizedImageField(size=[500, 500], upload_to='images/', blank=True, null=True)
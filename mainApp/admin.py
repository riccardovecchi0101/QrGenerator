from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Profile._meta.fields]


admin_site = admin.site

admin_site.register(Profile, ProfileAdmin)



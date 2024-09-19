from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CustomUser._meta.fields]


admin_site = admin.site

admin_site.register(CustomUser, CustomUserAdmin)
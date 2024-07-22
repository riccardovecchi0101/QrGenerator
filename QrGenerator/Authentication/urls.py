# Import necessary modules
from django.contrib import admin  # Django admin module
from django.urls import path  # URL routing
from .views import *  # Import views from the authentication app


# Define URL patterns
urlpatterns = [
    path('home/', home, name="home"),  # Home page
    path("", empty, name="home2"),
    path('login/', login_page, name='login_page'),  # Login page
    path('register/', register_page, name='register'),  # Registration page
    path('success/', success_page, name='success')
]


# Import necessary modules
from django.contrib import admin  # Django admin module
from django.urls import path  # URL routing
from .views import *  # Import views from the authentication app

app_name = 'authentication'
# Define URL patterns
urlpatterns = [
    path('login', login_page, name='login'),  # Login page
    path('register', register_page, name='register'),  # Registration page
    path('success', success_page, name='success')
]


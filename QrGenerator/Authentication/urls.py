# Import necessary modules
from django.contrib import admin  # Django admin module
from django.urls import path, include  # URL routing
from . import views

app_name = 'authentication'
# Define URL patterns
urlpatterns = [
    path('login/', views.login_page, name='login'),  # Login page
    path('register/', views.register_page, name='register'),  # Registration pag
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]


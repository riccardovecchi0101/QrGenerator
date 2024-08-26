from django.urls import path, include  # URL routing
from . import views


app_name = 'mainApp'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('hub/', views.hub_page, name='hub'),
    path('create/', views.create_project, name='project_creator'),
]


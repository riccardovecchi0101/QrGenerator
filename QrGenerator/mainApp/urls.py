from django.urls import path, include  # URL routing
from . import views


app_name = 'mainApp'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('hub/', views.hub_page, name='hub'),
    path('create/', views.create_project, name='project_creator'),
    path('edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('qr/<int:project_id>/', views.create_qr, name='create_qr')
]


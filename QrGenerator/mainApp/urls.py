from django.urls import path, include  # URL routing
from . import views


app_name = 'mainApp'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('hub/', views.hub_page, name='hub'),
    path('hub/logout', views.logout_view, name='logout'),
    path('create/', views.create_project, name='project_creator'),
    path('edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('qr/<int:project_id>/', views.create_qr, name='create_qr'),
    path('qr/<int:project_id>/maker/', views.qr_maker, name='qr_maker'),
    path('qr/<int:qr_id>/deleter', views.qr_deleter, name='qr_deleter'),
    path('qr/<int:project_id>/redirect_to_site', views.redirect_to_site, name='real_site')
]


from django.urls import path, include  # URL routing
from .views import *


app_name = 'mainApp'
urlpatterns = [
    path('', home_page, name='home'),
    path('hub/', hub_page, name='hub')
]


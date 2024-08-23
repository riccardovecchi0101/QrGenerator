
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def home_page(request):
    return render(request, "home.html")

def hub_page(request):
    return render(request, "hub.html")
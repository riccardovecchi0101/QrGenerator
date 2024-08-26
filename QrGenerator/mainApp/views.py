from django.utils import timezone
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
def home_page(request):
    return render(request, "home.html")

def hub_page(request):
    return render(request, "hub.html")


def create_project(request):
    if request.method == 'POST':
        date = timezone.datetime.now()
        title = request.POST.get('title')
        description = request.POST.get('description')
        print('title is' + str(title) +'and description is' + str(description) )

        if not title or not description:
            return render(request, 'hub.html', {'error': 'Title and description are required.'})

        current_project = Project.objects.create(description=description, title=title, date=date)
        current_user = request.user
        project_owner = Profile.objects.get(user=current_user)
        ProjectProfile.objects.create(owner=project_owner, project=current_project)

    return render(request, 'hub.html')


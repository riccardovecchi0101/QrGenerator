from io import BytesIO

from django.core.files.base import ContentFile
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
from django.shortcuts import render, redirect
import segno


def home_page(request):
    return render(request, "home.html")


def hub_page(request):
    current_user = request.user
    user_profile = Profile.objects.get(user=current_user)
    my_projects = ProjectProfile.objects.filter(owner=user_profile)
    projects = [profile.project for profile in my_projects]
    qrs = Qr.objects.all()

    return render(request, "hub.html", {'projects': projects, 'qrs': qrs})


def create_project(request):
    if request.method == 'POST':
        date = timezone.datetime.now()
        title = request.POST.get('title')
        description = request.POST.get('description')
        print('title is' + str(title) + 'and description is' + str(description))

        if not title or not description:
            return render(request, 'hub.html', {'error': 'Title and description are required.'})

        current_project = Project.objects.create(description=description, title=title, date=date)
        current_user = request.user
        project_owner = Profile.objects.get(user=current_user)
        ProjectProfile.objects.create(owner=project_owner, project=current_project)

        return render(request, 'hub.html', {'project': current_project})


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project.delete()
        return redirect('mainApp:hub')

    return render(request, 'hub.html', {'project': project})


def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title and description:
            project.title = title
            project.description = description
            project.save()
            return redirect('mainApp:hub')
        else:
            return render(request, 'mainApp:hub', {'error': 'Title and description are required.'})

    return render(request, 'mainApp:hub', {'project': project})


def create_qr(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        site_link = request.POST.get('sitelink')
        site_qr = segno.make(site_link)

        qr_number = project.qr_number
        project.qr_number += 1
        project.save()

        image_io = BytesIO()
        site_qr.save(image_io, kind='png', scale=7)
        image_io.seek(0)  # Reset del puntatore di lettura

        image_filename = f'{project.title}_{qr_number}.png'

        qr_instance = Qr(project=project)
        qr_instance.image.save(image_filename, ContentFile(image_io.read()), save=True)

    return redirect('mainApp:hub')

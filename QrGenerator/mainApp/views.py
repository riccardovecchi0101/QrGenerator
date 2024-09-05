from io import BytesIO

import qrcode
from django.core.files.base import ContentFile
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.shortcuts import render, redirect
import segno
from PIL import Image
import io


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
        link = request.POST.get('link')
        print('title is ' + str(title) + '  description is ' + str(description) + ' and link is ' + str(link))

        if not title or not description:
            return render(request, 'hub.html', {'error': 'Title and description are required.'})

        current_project = Project.objects.create(description=description, title=title, date=date, link=link)
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
        link = request.POST.get('link')

        if title or description or link:
            if title:
                project.title = title
            if description:
                project.description = description
            if link:
                project.link = link

            project.save()
            return redirect('mainApp:hub')
        else:
            return render(request, 'mainApp:hub', {'error': 'Title and description are required.'})

    return render(request, 'mainApp:hub', {'project': project})


def create_qr(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'GET':
        return render(request, "QrMaker.html", context={'project': project})

    return redirect('mainApp:hub')


def qr_maker(request, project_id):
    print("entered qrmaker view")
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        site_link = project.link
        fg_color = request.POST.get('fg_color')
        bg_color = request.POST.get('bg_color')
        image = request.FILES.get('image')

        print(f"site link is: {site_link} colors are: {fg_color}, {bg_color} image is: {image}")

        qr = qrcode.QRCode(version=1,
                           box_size=10,
                           border=5)

        # Adding data to the instance 'qr'
        qr.add_data(site_link)

        qr.make(fit=True)
        img = qr.make_image(fill_color=fg_color,
                            back_color=bg_color)
        image_filename = f'{project.title}_{project.qr_number}.png'

        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)


        qr_instance = Qr(project=project)
        qr_instance.image.save(image_filename, ContentFile(img_byte_arr.read()) , save=True)

        project.qr_number += 1
        project.save()

    return redirect("mainApp:hub")


def redirect_to_site(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    redirect(project.link)


import os
from io import BytesIO

import django.http
import qrcode
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
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

    qr_list = []
    for project in projects:
        for qr in Qr.objects.filter(project=project):
            qr_list.append(qr)

    return render(request, "hub.html", {'projects': projects, 'qrs': qr_list})


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
        qr_list = []

        for qr in Qr.objects.filter(project=project):
            qr_list.append(qr)

        for qr in qr_list:
            os.remove(qr.image.path)

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
        preview = request.POST.get('preview')
        value = request.POST.get('value')
        image = request.FILES.get('image')

        print(f"site link is: {site_link} colors are: {fg_color}, {bg_color} image is: {image} preview is {preview}")

        qr = qrcode.QRCode(version=5,
                           box_size=10,
                           error_correction=qrcode.constants.ERROR_CORRECT_H,
                           border=5)

        qr.add_data(site_link)

        qr.make(fit=True)
        img = qr.make_image(fill_color=fg_color,
                            back_color=bg_color).convert('RGB')

        if image:
            logo = Image.open(image)

            basewidth = 100

            logo = logo.resize((150, 150))


            pos = ((img.size[0] - logo.size[0]) // 2,
                   (img.size[1] - logo.size[1]) // 2)

            img.paste(logo, pos)

        image_filename = f'{project.title}_{project.qr_number}.png'

        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        if preview:
            response = HttpResponse(img_byte_arr, content_type='image/png')
            response['Content-Disposition'] = 'inline'; filename="qrcode.png"
            return response

        qr_instance = Qr(project=project)
        qr_instance.image.save(image_filename, ContentFile(img_byte_arr.read()), save=True)

        project.qr_number += 1
        project.save()

    return redirect("mainApp:hub")


def redirect_to_site(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    redirect(project.link)


def qr_deleter(request, qr_id):
    qr = get_object_or_404(Qr, id=qr_id)
    if request.method == "POST":
        qr.project.qr_number -= 1
        qr.project.save()
        os.remove(qr.image.path)
        qr.delete()
        return redirect('mainApp:hub')

    return render(request, 'hub.html')

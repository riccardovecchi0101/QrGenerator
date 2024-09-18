import os
from io import BytesIO
import django.http
import qrcode
from PIL.ImageDraw import ImageDraw
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from PIL import Image, ImageDraw, ImageFont


def home_page(request):
    try:
        return render(request, "mainApp/home.html")
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


def logout_view(request):
    try:
        logout(request)
        return redirect('mainApp:home')
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


@login_required
def hub_page(request):
    try:
        current_user = request.user
        user_profile = Profile.objects.get(user=current_user)
        my_projects = ProjectProfile.objects.filter(owner=user_profile)
        projects = [profile.project for profile in my_projects]

        qr_list = []
        for project in projects:
            for qr in Qr.objects.filter(project=project):
                qr_list.append(qr)

        return render(request, "mainApp/hub.html", {'projects': projects, 'qrs': qr_list})
    except Profile.DoesNotExist:
        return HttpResponse("Profile not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


def create_project(request):
    try:
        if request.method == 'POST':
            date = timezone.datetime.now()
            title = request.POST.get('title')
            description = request.POST.get('description')
            link = request.POST.get('link')
            if not link.startswith(('http://', 'https://')):
                link = 'https://' + link

            if not title:
                title="No title"
            if not description:
                description="No description"

            current_project = Project.objects.create(description=description, title=title, date=date, link=link)
            current_user = request.user
            project_owner = Profile.objects.get(user=current_user)
            ProjectProfile.objects.create(owner=project_owner, project=current_project)

            return render(request, 'mainApp/hub.html', {'project': current_project})
    except Profile.DoesNotExist:
        return HttpResponse("Profile not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


def delete_project(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        if request.method == 'POST':
            qr_list = [qr for qr in Qr.objects.filter(project=project)]
            for qr in qr_list:
                if qr.image and os.path.exists(qr.image.path):
                    os.remove(qr.image.path)
            project.delete()
            return redirect('mainApp:hub')
        return render(request, 'mainApp/hub.html', {'project': project})
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


def edit_project(request, project_id):
    try:
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
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


def create_qr(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        if request.method == 'GET':
            return render(request, "mainApp/QrMaker.html", context={'project': project})
        return redirect('mainApp:hub')
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


def qr_maker(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        qr_instance = Qr(project=project)

        if request.method == 'POST':
            fg_color = request.POST.get('fg_color')
            bg_color = request.POST.get('bg_color')
            preview = request.POST.get('preview')
            value = request.POST.get('value')
            image = request.FILES.get('image')
            label = request.POST.get('LabelLogo')
            color = request.POST.get('LabelColor')

            if not preview:
                qr_instance.save()
                link = reverse('mainApp:real_site', kwargs={'project_id': project_id, 'qr_id': qr_instance.id})
                url = request.build_absolute_uri(link)
                site_link = url
            else:
                site_link = ''

            qr = qrcode.QRCode(version=5, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_H, border=5)
            qr.add_data(site_link)
            qr.make(fit=True)
            img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert('RGBA')

            if label:
                if not color:
                    color = 'black'
                label_image = create_text_image(label, text_color=color)
                pos = ((img.size[0] - label_image.size[0]) // 2, (img.size[1] - label_image.size[1]) // 2)
                img.paste(label_image, pos)
            elif image:
                logo = Image.open(image).convert("RGBA")
                alpha = logo.getchannel('A')
                alpha = alpha.point(lambda p: min(255, int(p * 10.0)))
                logo.putalpha(alpha)
                logo = logo.resize((150, 150))
                pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
                img.paste(logo, pos, logo)

            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            if preview:
                response = HttpResponse(img_byte_arr, content_type='image/png')
                response['Content-Disposition'] = 'inline; filename="qrcode.png"'
                return response

            qr_instance.image.save(f'{project.title}_{project.qr_number}.png', ContentFile(img_byte_arr.read()), save=True)
            project.qr_number += 1
            project.save()

        return redirect("mainApp:hub")
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


def redirect_to_site(request, project_id, qr_id):
    try:
        project = get_object_or_404(Project, id=project_id)

        qr = get_object_or_404(Qr, id=qr_id)
        qr.times_scanned += 1
        qr.save()

        return redirect(project.link)
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)
    except Qr.DoesNotExist:
        return HttpResponse("QR code not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


def qr_deleter(request, qr_id):
    try:
        qr = get_object_or_404(Qr, id=qr_id)
        if request.method == "POST":
            qr.project.qr_number -= 1
            qr.project.save()
            if qr.image and os.path.exists(qr.image.path):
                os.remove(qr.image.path)
            qr.delete()
            return redirect('mainApp:hub')
        return render(request, 'mainApp/hub.html')
    except Qr.DoesNotExist:
        return HttpResponse("QR code not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


def project_info(request, project_id):
    try:
        total_scans = 0
        project = get_object_or_404(Project, id=project_id)
        qr_list = [qr for qr in Qr.objects.filter(project=project)]

        for qr in qr_list:
            total_scans += qr.times_scanned
        return render(request, 'mainApp/project_info.html', context={'project': project, 'project_qrs': qr_list, 'total_scans':total_scans})
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)
def create_text_image(text,  text_color, font_size=40, image_size=(300, 100)):
    """
    Crea un'immagine contenente solo il testo, con sfondo trasparente.

    :param text: Testo da scrivere nell'immagine.
    :param font_size: Dimensione del font.
    :param image_size: Dimensioni dell'immagine (larghezza, altezza).
    :param text_color: Colore del testo in formato RGBA.
    :return: Oggetto immagine PIL.
    """
    # Crea un'immagine con sfondo trasparente (RGBA)
    img = Image.new('RGBA', image_size, (255, 255, 255, 0))  # Trasparenza totale con (A=0)

    # Carica un font predefinito
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()


    draw = ImageDraw.Draw(img)


    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)


    draw.text(position, text, font=font, fill=text_color)

    return img
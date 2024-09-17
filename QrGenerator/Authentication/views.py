# Import necessary modules and models
import re

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from QrGenerator import settings
from .models import *
from mainApp.models import Profile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode

from django.core.validators import RegexValidator


User = get_user_model()


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        rememberme = request.POST.get('rememberMe')

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)

                if not rememberme:
                    request.session.set_expiry(0)

                return redirect('mainApp:hub')
            else:
                messages.info(request, 'Verifica la tua email per attivare l\'account.')
                return redirect('authentication:login')
        else:
            messages.error(request, "Username o password non validi.")
            return redirect('authentication:login')

    return render(request, 'login.html')


# Define a view function for the registration page
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.filter(username=username)
        user_email = User.objects.filter(email=email)

        if user.exists() or user_email.exists():
            messages.info(request, "Username or Email already taken!")
            return redirect('authentication:register')


        if not validate_pw(password):
            messages.info(request, 'La password deve contenere solo caratteri alfanumerici, può contenere \".\" e deve contenere una maiuscola.')
            return redirect('authentication:register')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )

        Profile.objects.create(user=user)


        user.set_password(password)
        user.is_active = False  # Imposta l'utente come inattivo fino alla verifica
        user.save()

        # Genera un token e una URL di conferma
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = request.build_absolute_uri(
            reverse('authentication:verify_email', args=[uid, token])
        )


        subject = 'Conferma la tua email'
        html_message = render_to_string('Authentication/email_confirmation.html', {
            'user': user,
            'verification_link': verification_link
        })
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, [email], html_message=html_message)

        messages.info(request, "Account creato con successo! Controlla la tua email per confermare.")



    return render(request, 'login.html')





def validate_pw(s):
    pattern = r'^(?=.*\d)(?=.*[A-Z])[a-zA-Z0-9.]+$'
    if re.match(pattern, s):
        return True
    else:
        return False




def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model()._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email confermata con successo!")
    else:
        messages.error(request, "Il link di conferma non è valido.")

    return redirect('authentication:login')
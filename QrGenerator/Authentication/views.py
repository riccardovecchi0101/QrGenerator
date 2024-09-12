# Import necessary modules and models
import re

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from mainApp.models import Profile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode

from django.core.validators import RegexValidator


User = get_user_model()

# Define a view function for the login page
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        rememberme = request.POST.get('rememberMe')


        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('authentication:login')

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('authentication:login')
        else:
            # Log in the user and redirect to the home page upon successful login
           # if not request.user.is_email_verified:
            #    return HttpResponse('Per favore verifica la tua email per accedere a questa pagina.')
            login(request, user)
            if not rememberme:
                request.session.set_expiry(0)
            return redirect('mainApp:hub')

    # Render the login page template (GET request)
    return render(request, 'login.html')


# Define a view function for the registration page
def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)

        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('authentication:register')

        # Create a new User object with the provided information
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
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()

    #   send_verification_email(user, request)


        # Display an information message indicating successful account creation
        messages.info(request, "Account creato con successo")
        return redirect('authentication:login')

    # Render the registration page template (GET request)
    return render(request, 'register.html')



def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_link = request.build_absolute_uri(
        f'/verify-email/{uid}/{token}/'
    )
    subject = 'Verifica la tua email'
    message = f'Per favore, clicca sul seguente link per verificare la tua email: {verification_link}'

    user.email_user(subject, message)



def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return HttpResponse('Email verificata con successo.')
    else:
        return HttpResponse('Link non valido o scaduto.')



def validate_pw(s):
    pattern = r'^(?=.*\d)(?=.*[A-Z])[a-zA-Z0-9.]+$'
    if re.match(pattern, s):
        return True
    else:
        return False
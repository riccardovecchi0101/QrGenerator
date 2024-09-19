# Import necessary modules
from django.template.defaulttags import url
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetConfirmView

app_name = 'authentication'

urlpatterns = [

    path('login/', views.login_page, name='login'),  # Login page
    path('register/', views.register_page, name='register'),  # Registration page
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html", email_template_name="email_pw.html",success_url = reverse_lazy('authentication:password_reset_done')),
         name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(template_name="password_reset_confirm.html", success_url = reverse_lazy('authentication:password_reset_complete')),
         name='password_reset_confirm'),

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_success.html"),
         name='password_reset_complete'),
]
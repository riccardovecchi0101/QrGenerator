from django import forms
from django.contrib.auth.forms import SetPasswordForm

class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        return password
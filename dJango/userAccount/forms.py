from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class CreateAccountForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput()
        }


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class CreateAccountForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }


class CustomUserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'is_staff', 'groups']
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
            'username': forms.HiddenInput()
        }

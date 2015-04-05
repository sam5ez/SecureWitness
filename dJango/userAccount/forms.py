from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


# class PasswordField(forms.CharField):
# widget = forms.PasswordInput()
#
#
# class CreateAccountForm(forms.Form):
# username = forms.CharField(max_length=30)
#     password = PasswordField()
#     email = forms.EmailField()
#     first_name = forms.CharField(max_length=30,label="First Name", required=False)
#     last_name = forms.CharField(max_length=30,label="Last Name", required=False)

class CreateAccountForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput()
        }

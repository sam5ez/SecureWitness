from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import CreateAccountForm
import datetime


def create_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                     last_name=last_name,last_login=datetime.datetime.now())
            context = {'username': username, 'succeed': True}
        else:
            context = {'form': form, 'succeed': False}
        return render(request, "create_account_result.html", context)
    else:
        return render(request, "create_account.html", {'form': CreateAccountForm()})
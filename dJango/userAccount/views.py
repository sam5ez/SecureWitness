import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth

from .forms import CreateAccountForm, LoginForm


def create_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            if not user.last_login:
                user.last_login = datetime.datetime.now()
            context = {'username': username, 'succeed': True}
        else:
            context = {'form': form, 'succeed': False}
        return render(request, "create_account_result.html", context)
    else:
        return render(request, "create_account.html", {'form': CreateAccountForm()})


def auth_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/user_home/')
        else:
            message = 'Authentication fail.'
    else:
        message = ''
    return render(request, "user_auth.html", {'form': LoginForm(), 'message': message})


def user_home(request):
    return render(request, 'user_home.html', {})
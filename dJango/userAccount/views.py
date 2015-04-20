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
    return render(request, 'user_home.html', {'user': request.user})


def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return render(request, "user_auth.html", {'form': LoginForm(), 'message': 'Successfully logged out.'})
    else:
        return auth_view(request)

from .forms import CustomUserChangeForm


def manage_user(request):
    if not request.user.is_staff:
        return render(request, "user_home.html", {'user': request.user})
    else:
        message = {}
        user_list = User.objects.all()
        if request.method == 'POST':
            obj_user = list(User.objects.filter(username__exact=request.POST.get("username", "")))[0]
            message['obj_name'] = obj_user.username
            if '_confirm_delete' in request.POST:
                obj_user.delete()
                message['brief'] = "Success"
                message['type'] = "info"
                message['main'] = "This user has been deleted:"
            change_form = CustomUserChangeForm(request.POST, instance=obj_user)
            if change_form.is_valid():
                if '_try_delete' in request.POST:
                    message['type'] = "danger"
                    message['brief'] = "Warning"
                    message['main'] = "Are you sure you want to delete this user:"
                    message['need_confirm'] = True
                if '_edit' in request.POST:
                    change_form.save()
                    message['type'] = "success"
                    message['brief'] = "Success"
                    message['main'] = "This user has been updated:"
                    # return render(request, "manage_user.html",{'message':})
            else:  # form is invalid
                message['type'] = "warning"
                message['brief'] = "Error"
                message['main'] = "There is some error processing your request..."
        form_list = []
        for user in user_list:
            form = CustomUserChangeForm(instance=user)
            form_list.append(form)
        return render(request, "manage_user.html",
                      {'form_list': form_list, 'message': message})

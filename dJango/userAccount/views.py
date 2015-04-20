import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from uploadFile.models import Report
from django.contrib import auth
from uploadFile.forms import CustomReportChangeForm

from .forms import CreateAccountForm, LoginForm, GroupCreationForm, AddUserToGroupForm


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


from .forms import CustomUserChangeForm, CustomGroupChangeForm


def manage_user(request):
    if not request.user.is_staff:
        return render(request, "user_home.html", {'user': request.user})
    else:
        message = {}
        user_list = User.objects.all()
        if request.method == 'POST':
            l = list(User.objects.filter(username__exact=request.POST.get("username", "")))
            obj_user = None
            if len(l) != 0:
                obj_user = l[0]
                message['obj_name'] = obj_user.username

            if '_confirm_delete' in request.POST:
                obj_user.delete()
                message['brief'] = "Success"
                message['type'] = "info"
                message['main'] = "This user has been deleted:"
            else:
                change_form = CustomUserChangeForm(request.POST, instance=obj_user)
                if change_form.is_valid():
                    if '_try_delete' in request.POST:
                        message['type'] = "danger"
                        message['brief'] = "Warning"
                        message['main'] = "Are you sure you want to delete this user?"
                        message['need_confirm'] = True
                    if '_edit' in request.POST:
                        change_form.save()
                        message['type'] = "success"
                        message['brief'] = "Success"
                        message['main'] = "This user has been updated:"
                else:  # form is invalid
                    message['type'] = "warning"
                    message['brief'] = "Error"
                    message['main'] = "There is some error processing your request..."
        form_list = []
        for user in user_list:
            form = CustomUserChangeForm(instance=user)
            form_list.append(form)
        return render(request, "manage_user.html",
                      {'form_list': form_list, 'message': message, 'user': request.user})


def manage_group(request):
    if not request.user.is_staff:
        return render(request, "user_home.html", {'user': request.user})
    else:
        message = {}
        group_list = Group.objects.all()
        if request.method == 'POST':
            l = list(Group.objects.filter(name__exact=request.POST.get("name", "")))
            obj_group = None
            if len(l) != 0:
                obj_group = l[0]
                message['obj_name'] = obj_group.name
            if '_create' in request.POST:
                creation_form = GroupCreationForm(request.POST)
                if creation_form.is_valid():
                    creation_form.save()
                    message['type'] = "success"
                    message['brief'] = "Success"
                    message['main'] = "This group has been created:"
                else:
                    message['type'] = "warning"
                    message['brief'] = "Error"
                    message['main'] = "There is some error creating the group..."
            elif '_confirm_delete' in request.POST:
                obj_group.delete()
                message['type'] = "info"
                message['brief'] = "Success"
                message['main'] = "This group has been deleted:"
            else:
                change_form = CustomGroupChangeForm(request.POST, instance=obj_group)
                if change_form.is_valid():
                    if '_try_delete' in request.POST:
                        message['type'] = "danger"
                        message['brief'] = "Warning"
                        message['main'] = "Are you sure you want to delete this group:"
                        message['need_confirm'] = True
                    if '_save' in request.POST:
                        change_form.save()
                        message['type'] = "success"
                        message['brief'] = "Success"
                        message['main'] = "This group has been updated:"
                else:  # form is invalid
                    message['type'] = "warning"
                    message['brief'] = "Error"
                    message['main'] = "There is some error processing your request..."
        form_list = []
        for group in group_list:
            form = CustomGroupChangeForm(instance=group)
            form_list.append(form)
        return render(request, "manage_group.html",
                      {'form_list': form_list, 'message': message, 'user': request.user,
                       'group_creation_form': GroupCreationForm()})


def my_groups(request):
    message = {}
    if request.method == 'POST':
        gp_name = request.POST.get('name', '')
        group = Group.objects.get(name=gp_name)
        add_user_form = AddUserToGroupForm(request.POST, instance=group)
        if add_user_form.is_valid():
            # user_to_be_added = User.objects.get(username=add_user_form.cleaned_data['user_to_be_added'])
            # g = Group.objects.get(name=add_user_form.cleaned_data['group'])
            g = add_user_form.save()
            if g is not None:
                message['type'] = "success"
                message['brief'] = "Success"
                message['main'] = "Successfully added the user to the group or the user is already in the group."
            else:
                message['type'] = "warning"
                message['brief'] = "Fail"
                message['main'] = "OH! Please try again and make sure you enter the correct username."

    else:
        add_user_form = AddUserToGroupForm()
    form_list = []

    for group in request.user.groups.all():
        form = AddUserToGroupForm(instance=group)
        form_list.append(form)

    return render(request, 'my_groups.html',
                  {'form_list': form_list, 'add_user_form': add_user_form, 'message': message})


def manage_reports(request):
    reports = []
    message = {}
    if request.method == 'POST':
        rep = Report.objects.get(title=request.POST.get("title", ""))
        message['rep_name'] = rep.title
        if '_confirm_delete' in request.POST:
            rep.delete()
            message['brief'] = "Success"
            message['type'] = "info"
            message['main'] = "This report has been deleted:"
        change_form = CustomReportChangeForm(request.POST, instance=rep)
        if change_form.is_valid():
            if '_try_delete' in request.POST:
                message['type'] = "danger"
                message['brief'] = "Warning"
                message['main'] = "Are you sure you want to delete this report?"
                message['need_confirm'] = True
        else:
            message['type'] = "warning"
            message['brief'] = "Error"
            message['main'] = "There is some error processing your request..."
    for report in Report.objects.all():
        form = CustomReportChangeForm(instance=report)
        reports.append(form)
    return render(request, 'manage_reports.html', {'reports': reports, 'message': message})
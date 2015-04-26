from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from django.contrib.admin.widgets import FilteredSelectMultiple


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
        fields = ['username', 'is_staff', 'is_active', 'groups']
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
            'username': forms.HiddenInput()
        }


class CustomGroupChangeForm(ModelForm):
    user_list = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                               widget=FilteredSelectMultiple('Users', False),
                                               required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.get('initial', {})
            initial['user_list'] = instance.user_set.all()
            kwargs['initial'] = initial
        super(CustomGroupChangeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        group = super(CustomGroupChangeForm, self).save(commit=commit)
        if commit:
            group.user_set = self.cleaned_data['user_list']
        else:
            old_save_m2m = self.save_m2m

            def new_save_m2m():
                old_save_m2m()
                group.user_set = self.cleaned_data['user_list']

            self.save_m2m = new_save_m2m
        return group

    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.HiddenInput()
        }


class GroupCreationForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class AddUserToGroupForm(ModelForm):
    user_list = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                               widget=FilteredSelectMultiple('Users', False),
                                               required=False)
    user_to_be_added = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.get('initial', {})
            initial['user_list'] = instance.user_set.all()
            kwargs['initial'] = initial
        super(AddUserToGroupForm, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        group = super(AddUserToGroupForm, self).save()
        try:
            u = User.objects.get(username=self.cleaned_data['user_to_be_added'])
        except User.DoesNotExist:
            u = None
        if u is not None:
            group.user_set.add(u)
            return group
        else:
            return None

    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.HiddenInput()
        }

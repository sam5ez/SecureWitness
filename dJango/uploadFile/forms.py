from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User,Group

from .models import Report


class ReportForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Report
        fields = ['title', 'file', 'short_desc', 'detailed_desc', 'location', 'tag', 'private', 'groups']
        labels = {
            "short_desc": _("Short Description"),
            "detailed_desc": _("Detailed Description"),
            "private": _("Mark as private (only specified group and I can see the report)"),
            "groups": _("Specify which group(s) can see the report")
        }
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            "short_desc": forms.Textarea(attrs={'class': 'form-control'}),
            "detailed_desc": forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        uploader = User.objects.get(username=kwargs.pop('uploader'))
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['groups'].queryset = uploader.groups


class SearchForm(forms.Form):
    error_css_class = 'error'
    title = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sub_date = forms.DateTimeField(label='submission date', required=False,
                                   widget=SelectDateWidget)
    description = forms.CharField(max_length=100, required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))


class CustomReportChangeForm(ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'short_desc', 'detailed_desc', 'location', 'tag', 'private', 'groups']
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            "short_desc": forms.Textarea(attrs={'class': 'form-control'}),
            "detailed_desc": forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.HiddenInput()
        }
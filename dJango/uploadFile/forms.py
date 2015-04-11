from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Report


class ReportForm(ModelForm):
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
            'groups': forms.CheckboxSelectMultiple()
        }


class SearchForm(forms.Form):
    title = forms.CharField(max_length=30, required=False)
    sub_date = forms.DateTimeField(label='submission date', required=False)
    description = forms.CharField(max_length=100, required=False)
    location = forms.CharField(max_length=30, required=False)
    tag = forms.CharField(max_length=30, required=False)
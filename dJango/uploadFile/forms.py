from django import forms
from django.forms import ModelForm
from .models import Report
from django.utils.translation import ugettext_lazy as _


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'file', 'short_desc', 'detailed_desc', 'location', 'tag', 'private']
        labels = {
            "short_desc": _("Short Description"),
            "detailed_desc": _("Detailed Description"),
            "private": _("Mark as private (only I can view this report)")
        }


class SearchForm(forms.Form):
    title = forms.CharField(max_length=30, required=False)
    sub_date = forms.DateTimeField(label='submission date', required=False)
    description = forms.CharField(max_length=100, required=False)
    location = forms.CharField(max_length=30, required=False)
    tag = forms.CharField(max_length=30, required=False)
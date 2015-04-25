from datetime import datetime

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import *


class ReportForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Report
        fields = ['reporter', 'title', 'file', 'short_desc', 'detailed_desc', 'location', 'event_date', 'tags',
                  'private', 'groups']
        labels = {
            "short_desc": _("Short Description"),
            "detailed_desc": _("Detailed Description"),
            "location": _("Where did it happened"),
            "event_date": _("When did it happened"),
            "private": _("Mark as private (only specified group and I can see the report)"),
            "groups": _("Specify which group(s) can see the report (only groups you are in are shown)")
        }
        widgets = {
            'reporter': forms.HiddenInput(),
            'groups': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            "short_desc": forms.Textarea(attrs={'class': 'form-control'}),
            "detailed_desc": forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': SelectDateWidget(years=range(1900, datetime.today().year)),
            'tags': FilteredSelectMultiple('Tags', False),
        }

    def __init__(self, *args, **kwargs):
        reporter = kwargs.pop('reporter')
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['reporter'].initial = reporter
        self.fields['groups'].queryset = reporter.groups
        # self.fields['event_date'] = forms.DateField(widget=SelectDateWidget,required=False)


class SearchForm(forms.Form):
    error_css_class = 'error'
    title = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    event_date = forms.DateTimeField(label='Event date', required=False,
                                     widget=SelectDateWidget)
    description = forms.CharField(max_length=100, required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))


class CustomReportChangeForm(ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'short_desc', 'detailed_desc', 'location', 'tags', 'private', 'groups']
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            "short_desc": forms.Textarea(attrs={'class': 'form-control'}),
            "detailed_desc": forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomReportChangeForm, self).__init__(*args, **kwargs)
        self.fields['groups'].queryset = self.instance.reporter.groups


class AddTagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            "name": _("new tag")
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'report', 'content']
        labels = {
            "content": _("New comment"),
            "author": _("Commenter")
        }
        widgets = {
            'author': forms.HiddenInput(),
            'report': forms.HiddenInput(),
            'content': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('at')
        rpt = kwargs.pop('report')
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = user
        self.fields['report'].initial = rpt
        self.fields['anonymous'] = forms.BooleanField(widget=forms.CheckboxInput(), required=False, initial=False)

    def __save__(self, commit=True):
        cmt = super(CommentForm, self).save(commit=commit)
        return cmt


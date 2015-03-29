from django.forms import ModelForm
from .models import Report


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'file', 'short_desc', 'detailed_desc', 'location', 'tag']

# from django import forms
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Report(models.Model):
    title = models.CharField(max_length=30)
    # author = User()
    file = models.FileField()
    sub_date = models.DateTimeField()
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    def file_link(self):
        if self.file:
            return "<a href='%s'>download</a>" % (self.file.url,)
        else:
            return "No attachment"


# class UploadFileForm(forms.Form):
#     title = forms.CharField(max_length=30)
#     file = forms.FileField()



# from django import forms
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Report(models.Model):
    # reporter = models.ForeignKey('User')
    title = models.CharField(max_length=30)
    sub_date = models.DateTimeField(auto_now_add=True, auto_created=True)
    short_desc = models.TextField(max_length=30, blank=True)  # blank=True: allow empty string
    detailed_desc = models.TextField(max_length=100, blank=True)
    location = models.CharField(max_length=30, blank=True)
    file = models.FileField(upload_to="reports")
    tag = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.title

    def file_link(self):
        if self.file:
            return "<a href='%s'>download</a>" % (self.file.url,)
        else:
            return "No attachment"

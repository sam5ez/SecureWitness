# from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class Report(models.Model):
    reporter = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    sub_date = models.DateTimeField(auto_now_add=True, auto_created=True)
    short_desc = models.TextField(max_length=30, blank=True)  # blank=True: allow empty string
    event_date = models.DateField(null=True, blank=True)
    detailed_desc = models.TextField(max_length=100, blank=True)
    location = models.CharField(max_length=30, blank=True)
    file = models.FileField(upload_to="reports")
    tags = models.ManyToManyField('Tag', blank=True)
    private = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return self.title

    def file_link(self):
        if self.file:
            return "<a href='%s'>download</a>" % (self.file.url,)
        else:
            return "No attachment"


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Comment(models.Model):
    report = models.ForeignKey(Report)
    date = models.DateTimeField(auto_now_add=True, auto_created=True)
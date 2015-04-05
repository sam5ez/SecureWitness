from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect
from .models import Report, User
from .forms import ReportForm, SearchForm
from django import forms


def upload_file(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form = form.save(commit=False)
            form.reporter = request.user
            form.save()
            context = {'success': True, 'form': form}
        else:
            context = {'success': False, 'form': form}
        return render(request, 'report_upload_result.html', context)
    else:
        form = ReportForm()
    return render(request, 'report_upload.html', {'form': form})


def search_file(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # file is saved
            title = form.cleaned_data['title']
            desc = form.cleaned_data['description']
            loc = form.cleaned_data['location']
            tag = form.cleaned_data['tag']
            r_list = Report.objects.filter(title__icontains=title).filter(
                Q(short_desc__icontains=desc) | Q(detailed_desc__icontains=desc)).filter(
                location__icontains=loc).filter(tag__icontains=tag)  # case-insensitive contain
            context = {'report_list': r_list, 'valid': True}
        else:
            context = {'report_list': [], 'valid': False}
        return render(request, 'report_search_result.html', context)
    else:
        form = SearchForm()
        return render(request, 'report_search.html', {'form': form})

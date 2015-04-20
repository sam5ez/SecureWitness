from django.shortcuts import render
from django.db.models import Q

from .models import Report
from .forms import ReportForm, SearchForm


def upload_file(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        # form.reporter = request.user
        if form.is_valid():
            # file is saved
            form_2 = form.save(commit=False)  # using commit=False will fail to save manytomany fields
            form_2.reporter = request.user
            form_2.save()
            form.save_m2m()
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
                location__icontains=loc).filter(tag__icontains=tag).filter(
                Q(reporter__exact=request.user) | Q(private=False) | Q(groups__in=request.user.groups.all())).distinct()
            context = {'report_list': r_list, 'valid': True}
        else:
            context = {'report_list': [], 'valid': False}
        return render(request, 'report_search_result.html', context)
    else:
        form = SearchForm()
        return render(request, 'report_search.html', {'form': form})
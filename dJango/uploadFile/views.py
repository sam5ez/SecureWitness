from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect

from .models import Report
from .forms import ReportForm, SearchForm, CustomReportChangeForm
from django.contrib import auth



def upload_file(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user_home/')
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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user_home/')
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


def my_reports(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/user_home/')
        reports = []
        message = {}
        if request.method == 'POST':
            rep = Report.objects.get(title=request.POST.get("title", ""))
            message['rep_name'] = rep.title
            if '_confirm_delete' in request.POST:
                rep.delete()
                message['brief'] = "Success"
                message['type'] = "info"
                message['main'] = "This report has been deleted:"
            change_form = CustomReportChangeForm(request.POST, instance=rep)
            if change_form.is_valid():
                if '_try_delete' in request.POST:
                    message['type'] = "danger"
                    message['brief'] = "Warning"
                    message['main'] = "Are you sure you want to delete this report?"
                    message['need_confirm'] = True
                if '_edit' in request.POST:
                    change_form.save()
                    message['type'] = "success"
                    message['brief'] = "Success"
                    message['main'] = "This report has been updated:"
            else:
                message['type'] = "warning"
                message['brief'] = "Error"
                message['main'] = "There is some error processing your request..."
        for report in Report.objects.all():
            if report.reporter == request.user:
                form = CustomReportChangeForm(instance=report)
                reports.append(form)
        return render(request, 'my_reports.html', {'reports': reports, 'message': message})

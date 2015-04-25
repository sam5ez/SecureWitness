from django.shortcuts import render

from django.db.models import Q
from django.http import HttpResponseRedirect

from .models import Report, Comment
from .forms import ReportForm, SearchForm, CustomReportChangeForm, AddTagForm, CommentForm


def upload_file(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/auth/')
    if request.method == 'POST':
        if "add_tag" in request.POST:
            f = AddTagForm(request.POST)
            if f.is_valid():
                f.save()
            return render(request, 'report_upload_result.html',
                          {'form': ReportForm(reporter=request.user), 'add_tag_form': AddTagForm()})

        form = ReportForm(request.POST, request.FILES, reporter=request.user)
        # form.reporter = request.user
        if form.is_valid():
            # file is saved
            form.save()
            context = {'success': True, 'form': form, 'add_tag_form': AddTagForm()}
        else:
            context = {'success': False, 'form': form, 'add_tag_form': AddTagForm()}
        return render(request, 'report_upload_result.html', context)
    else:
        form = ReportForm(reporter=request.user)
    return render(request, 'report_upload_result.html', {'form': form, 'add_tag_form': AddTagForm()})


def search_file(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/auth/')
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # file is saved
            title = form.cleaned_data['title']
            desc = form.cleaned_data['description']
            loc = form.cleaned_data['location']
            # tag = form.cleaned_data['tags']
            r_list = Report.objects.filter(title__icontains=title).filter(
                Q(short_desc__icontains=desc) | Q(detailed_desc__icontains=desc)).filter(
                location__icontains=loc).filter(
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
        return HttpResponseRedirect('/auth/')
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


def report_view(request, id):
    try:
        rpt = Report.objects.get(pk=id)
    except Report.DoesNotExist:
        return HttpResponseRedirect('/user_home/')
    if have_access_to_report(requester=request.user, report=rpt):
        message = ""
        if request.method == 'POST':
            form = CommentForm(data=request.POST, at=request.user, report=rpt)
            if form.is_valid():
                if form.cleaned_data['anonymous']:
                    f = form.save(commit=False)
                    f.author = None
                    f.save()
                    message = "Comment added by Anonymous."
                else:
                    form.save()
                    message = "Comment added by " + request.user.username + "."
            else:
                message = "Comment fails to save."
        else:
            form = CommentForm(at=request.user, report=rpt)
        comments = Comment.objects.filter(report__exact=rpt)
        return render(request, 'report_view.html',
                      {'report': rpt, 'comments': comments, 'cmt_form': form, 'message': message})
    else:
        return HttpResponseRedirect('/user_home/')


def have_access_to_report(requester, report):
    if (report.reporter == requester) | (not report.private):
        return True
    for group in report.groups.all():
        if group in requester.groups.all():
            return True
    return False


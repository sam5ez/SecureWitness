from django.shortcuts import render
from .models import Report
from django.db.models import Q
# Create your views here.


from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ReportForm, SearchForm


def upload_file(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            # return HttpResponseRedirect('/successful_upload/' + form.data.get('title') + '/')
            return successful_upload(request=request, title=form.data.get('title'))
    else:
        form = ReportForm()
    return render(request, 'upload_page.html', {'form': form})


def successful_upload(request, title):
    r_list = Report.objects.filter(title=title)
    r = r_list[0]
    context = {'tag': r.tag, 'title': title, 'sub_date': r.sub_date}
    return render(request, 'successful_upload.html', context)


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
    else:
        form = SearchForm()
        return render(request, 'report_search.html', {'form': form})
    return render(request, 'report_view.html', context)

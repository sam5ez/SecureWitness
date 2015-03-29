from django.shortcuts import render
from .models import Report
# Create your views here.


from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ReportForm


def upload_file(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/successful_upload/'+form.data.get('title')+'/')
    else:
        form = ReportForm()
    return render(request, 'upload_page.html', {'form': form})


def report_page(request, tag):
    r_list = Report.objects.filter(tag=tag)
    context = {'tag': tag, 'report_list': r_list}
    return render(request, 'report_view.html', context)


def successful_upload(request, title):
    r_list = Report.objects.filter(title=title)
    r = r_list[0]
    context = {'tag': r.tag, 'title': title, 'sub_date': r.sub_date}
    return render(request, 'successful_upload.html', context)
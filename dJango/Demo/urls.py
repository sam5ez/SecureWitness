from django.conf.urls import patterns, include, url
from django.contrib import admin
from uploadFile.views import success_upload,upload_file,show_report

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/success_upload/tit/$', success_upload),

    url(r'^report/(\d+)', show_report),
    url(r'^upload$', upload_file),
)

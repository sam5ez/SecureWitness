from django.conf.urls import patterns, include, url
from django.contrib import admin
from uploadFile.views import upload_file, search_file
from userAccount.views import create_account

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'Demo.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^upload/$', upload_file),
                       url(r'^search/$', search_file),
                       url(r'^create_account/$', create_account),
                       )

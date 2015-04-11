from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from uploadFile.views import upload_file, search_file
from userAccount.views import create_account, auth_view, user_home, logout


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'Demo.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^upload/$', upload_file),
                       url(r'^search/$', search_file),
                       url(r'^create_account/$', create_account),
                       url(r'^auth/$', auth_view),
                       url(r'^user_home/$', user_home),
                       url(r'^logout/$',logout)
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from mysites.views import CreateSite, DeleteSite, UpdateSite
from controller.views import ControllerDetailView, update_status, update_timeout, update_ssl, update_ping, \
    update_address, update_content_changed
from profiles.views import register, user_logout, user_login

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'profiles.views.index', name='index'),
                       url(r'^sites/create/$', login_required(CreateSite.as_view()), name='create_site'),
                       url(r'^sites/update/(?P<pk>\d+)/$', login_required(UpdateSite.as_view()), name='update_site'),
                       url(r'^sites/delete/(?P<pk>\d+)/$', login_required(DeleteSite.as_view()), name='delete_site'),
                       url(r'^controller/(?P<pk>\d+)/$', login_required(ControllerDetailView.as_view()),
                           name='controller_detail'),
                       url(r'^register/$', register, name='register'),
                       url(r'^login/$', user_login, name='login'),
                       url(r'^logout/$', user_logout, name='logout'),

                       url(r'^status/$', update_status, name='status'),
                       url(r'^timeout/$', update_timeout, name='timeout'),
                       url(r'^ssl/$', update_ssl, name='ssl'),
                       url(r'^ping/$', update_ping, name='ping'),
                       url(r'^address/$', update_address, name='address'),
                       url(r'^content_changed/$', update_content_changed, name='content_changed'),

                       # Note that by default this is also locked down with login:admin in app.yaml
                       url(r'^admin/', include(admin.site.urls)),
                       )

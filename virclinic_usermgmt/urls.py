from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'virclinic_usermgmt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$',views.register),
    url(r'^login/$',views.login_user),
    url(r'^logout/$',views.logout_user),
    url(r'^$',views.root),
    url(r'^home/$',views.home),
    url(r'^users/([0-9]+)$',views.users),
)

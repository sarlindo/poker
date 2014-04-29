from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'spt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('apps.spt.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^favicon.ico$', 'redirect_to', {'url': settings.STATIC_URL + 'favicon.ico'}),
)

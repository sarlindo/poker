from django.conf.urls import patterns, include, url

from apps.spt import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'spt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^pastsptwinners$', views.pastsptwinners, name='pastsptwinners'),
    url(r'^gamedetails$', views.gamedetails, name='gamedetails'),
    url(r'^profitloss$', views.profitloss, name='profitloss'),
    url(r'^stats$', views.stats, name='stats'),
    #url(r'^', views.IndexView.as_view(), name='home_list'),
)

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
    url(r'^get_profit$', views.get_profit, name='get_profit'),
    url(r'^get_placement$', views.get_placement, name='get_placement'),
    url(r'^get_placementwins$', views.get_placementwins, name='get_placementwins'),
    url(r'^get_plfinaltablewins$', views.get_plfinaltablewins, name='get_plfinaltablewins'),
    url(r'^get_profitbyseason$', views.get_profitbyseason, name='get_profitbyseason'),
    
    
    
    #url(r'^', views.IndexView.as_view(), name='home_list'),
)

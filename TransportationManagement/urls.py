from django.conf.urls import url
from . import views


app_name = 'TransportationManagement'
urlpatterns = [
    url(r'^$',views.index),
    url(r'^index/$', views.index, name='index'),
    url(r'^hello/$', views.hello, name='hello'),
    url(r'^accident/$', views.accident, name='accident'),
    url(r'^car/$', views.car, name='car'),
    url(r'^record/$', views.record, name='record'),
    url(r'^proposer/$', views.proposer, name='proposer'),
    url(r'^driver/$', views.driver, name='driver'),
    url(r'^login_view/$', views.driver, name='login_view'),
    url(r'^logout_view/$', views.driver, name='logout_view'),
    url(r'^ajax_submit/$', views.ajax_submit, name='logout_view'),
    url(r'^login/$', views.mylogin, name='mylogin'),
    url(r'^logout/$', views.mylogout, name='mylogout'),
]
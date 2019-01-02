from django.conf.urls import url
from . import views


app_name = 'TransportationManagement'
urlpatterns = [
    url(r'^$',views.need_login, name='login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^hello/$', views.hello, name='hello'),
    url(r'^test/$', views.test, name='test'),
    url(r'^accident/$', views.accident, name='accident'),
    url(r'^car/$', views.car, name='car'),
    url(r'^record/$', views.record, name='record'),
    url(r'^proposer/$', views.proposer, name='proposer'),
    url(r'^driver/$', views.driver, name='driver'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.mylogin, name='mylogin'),
    url(r'^logout/$', views.mylogout, name='mylogout'),
    url(r'^addcar/$', views.add_car, name='addcar'),
    url(r'^changecar/$', views.change_car, name='changecar'),
    url(r'^deletecar/$', views.delete_car, name='deletecar'),
    url(r'^adddriver/$', views.add_driver, name='adddriver'),
    url(r'^changedriver/$', views.change_driver, name='changedriver'),
    url(r'^deletedriver/$', views.delete_driver, name='deletedriver'),
    url(r'^addproposer/$', views.add_proposer, name='addproposer'),
    url(r'^changeproposer/$', views.change_proposer, name='changeproposer'),
    url(r'^deleteproposer/$', views.delete_proposer, name='deleteproposer'),
    url(r'^addrecord/$', views.add_record, name='addrecord'),
    url(r'^changerecord/$', views.change_record, name='changerecord'),
    url(r'^deleterecord/$', views.delete_record, name='deleterecord'),
    url(r'^addaccident/$', views.add_accident, name='addaccident'),
    url(r'^changeaccident/$', views.delete_car, name='changeaccident'),
    url(r'^deleteaccident/$', views.delete_accident, name='deleteaccident'),

]
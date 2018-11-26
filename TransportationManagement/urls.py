from django.conf.urls import url
from . import views

urlpatterns = [
    url('^hello/', views.hello),
    url('^Accident', views.accident),
    url('^Car', views.car),
    url('^Record', views.record),
    url('^Proposer', views.proposer),
    url('^Driver', views.driver),
]
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.user_login, name='index'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^grade/$', views.grade, name='grade'),
]
from django.http import HttpResponse
from . import views
from django.conf.urls import url

urlpatterns = [
  url(r'^$', views.index),
  url(r'register$', views.register),
  url(r'login$', views.login),
  url(r'^(?P<number>\d+)$', views.profile),
  url(r'logout$', views.logout),
  url(r'show$', views.show),

  # url(r'friends$', views.friends)
  # url(r'^users/(?P<id>\d+)$', views.profile),
  url(r'^(?P<number>\d+)/friend', views.friend),
  url(r'^(?P<number>\d+)/unfriend', views.unfriend),
  url(r'^(?P<number>\d+)/post', views.post),
  url(r'^(?P<number>\d+)/(?P<comment_id>\d+)/delete_comment', views.delete_comment),
  # url(r'^users/remove/(?P<id>\d+)$', views.remove_friend),
]
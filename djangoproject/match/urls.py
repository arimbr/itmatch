from django.conf.urls import patterns, url

from match import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^users/$', views.users, name='users'),
	url(r'^users/(?P<user_id>\d+)$', views.user, name='user'),
	url(r'^interests/$', views.interests, name='interests'),
	url(r'^interests/(?P<tag_id>\d+)$', views.interest, name='interest'),
)
from django.conf.urls import patterns, url

from match import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^profiles/$', views.profiles, name='profiles'),
	url(r'^profiles/(?P<profile_id>\d+)$', views.profile, name='profile'),
	url(r'^interests/$', views.interests, name='interests'),
	url(r'^interests/(?P<tag_id>\d+)$', views.interest, name='interest'),
	url(r'^register/$', views.register, name='register'),
)
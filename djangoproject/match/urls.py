from django.conf.urls import patterns, url

from match import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^profiles/$', views.profiles, name='profiles'),
	url(r'^profiles/(?P<profile_id>\d+)$', views.profile, name='profile'),
	url(r'^groups/$', views.groups, name='groups'),
	url(r'^groups/(?P<tag_id>\d+)$', views.group, name='group'),
	url(r'^signup/$', views.signup, name='signup'),
)
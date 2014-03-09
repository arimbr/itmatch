from django.conf.urls import patterns, url

from match import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^profile/(?P<user_id>\d+)$', views.profile, name='profile'),
)
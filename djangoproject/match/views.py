from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from match.models import Profile, Distance, Tag

def home(request):

	return render(request, 'match/home.html', {})

def profiles(request):

	profiles = Profile.objects.all()

	return render(request, 'match/profiles.html', {
		'profiles': profiles,
	})

def profile(request, profile_id):
	profile = get_object_or_404(Profile, pk=profile_id)
	return render(request, 'match/profile.html', {
		'profile': profile,
	})

def interests(request):
	tags = Tag.objects.all()

	return render(request, 'match/interests.html', {
		'tags': tags,
	})

def interest(request, tag_id):
	tag = get_object_or_404(Tag, pk=tag_id)

	return render(request, 'match/interest.html', {
		'tag': tag,
	})
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

def register(request):

	if request.method == "POST":

		name = request.POST["name"]
		selected_tags_ids = request.POST.getlist("tag")

		profile = Profile.objects.create(name=name)
		tags = Tag.objects.filter(id__in=selected_tags_ids)
		profile.tags.add(*tags)

		#selected tags will be a list of ids taken from the value input attribute.
		#For a checkbox it contains those checked
		#tag = Tag.objects.get(id=selected_tags[0])

		return HttpResponseRedirect('/profiles')

	else:

		tags = Tag.objects.all()

		return render(request, 'match/register.html', {
			'tags': tags,
		})

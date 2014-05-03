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

def groups(request):
	tags = Tag.objects.all()

	return render(request, 'match/interests.html', {
		'tags': tags,
	})

def group(request, tag_id):
	tag = get_object_or_404(Tag, pk=tag_id)

	return render(request, 'match/interest.html', {
		'tag': tag,
	})

def signup(request):

	if request.method == "POST":

		name = request.POST["name"] or "Anonymous"
		email = request.POST["email"]
		selected_tags_ids = request.POST.getlist("tag")
		#selected tags ids will be a list of ids taken from the value input attribute
		#For a checkbox it contains those checked
		#tag = Tag.objects.get(id=selected_tags[0])

		if not selected_tags_ids:
			errors = "select some interests"
			tags = Tag.objects.all()
			return render(request, 'match/register.html', {
				'tags': tags,
				'name': name,
				'email': email,
				'errors': errors,
			})

		profile = Profile.objects.create(name=name, email=email)
		tags = Tag.objects.filter(id__in=selected_tags_ids)
		profile.tags.add(*tags) # in models tags_changed() signal to add distances

		return HttpResponseRedirect('/profiles/' + '%s' % profile.id )

	else:

		tags = Tag.objects.all()

		return render(request, 'match/register.html', {
			'tags': tags,
		})

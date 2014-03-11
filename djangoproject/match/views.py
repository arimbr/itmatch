from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from match.models import User, Distance, Tag

def home(request):

	return render(request, 'match/home.html', {})

def users(request):

	users = User.objects.all()

	return render(request, 'match/users.html', {
		'users': users,
	})

def user(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	return render(request, 'match/user.html', {
		'user': user,
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
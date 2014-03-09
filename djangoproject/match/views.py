from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from match.models import User, Distance, Tag

def home(request):

	users = User.objects.all()

	return render(request, 'match/home.html', {
		'users': users,
	})

def profile(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	return render(request, 'match/profile.html', {
		'user': user,
	})
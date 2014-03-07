from django.shortcuts import render

from match.models import User, Distance, Tag

def home(request):

	users = User.objects.all()[:10]

	return render(request, 'match/home.html', {
		'users': users,
	})
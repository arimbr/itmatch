#python manage.py shell
#execfile('loadata.py')

from match.models import User, Tag, Distance

from utils.jsontools import read_json

users = read_json("utils/data/users.json")

tags = read_json("utils/data/tags.json")

#tanimoto
def tanimoto(u1, u2):
	"""
	u1, u2 are user instances from a queryset
	returns number between 0.0 and 1.0
	"""
	t1 = u1.tags.all()
	t2 = u2.tags.all()

	c1 = len(t1)
	c2 = len(t2)
	shr = len(set(t1).intersection(t2))

	try:
		return 1 - float(shr)/(c1 + c2 - shr)
	except ZeroDivisionError:
		return 1.0

#Populate Tag table
def load_tags(tags, Tag):
	for tag in tags:
		Tag.objects.create(name=tag)

#Populate User table
def load_users(users, User, Tag):
	for user, tags in users.iteritems():
		u = User.objects.create(name=user)
		ts = []

		for tag in tags:
			t = Tag.objects.get(name=tag)
			ts.append(t)

		u.tags.add(*ts)

#Populate Distance table
def load_distances(User, Distance):
	users = User.objects.all()
	for from_user in users:
		distances = []

		for to_user in users:
			d = tanimoto(from_user, to_user)
			distance = Distance.objects.create(from_user=from_user, to_user=to_user, d=d)
			distances.append(distance)

		from_user.distances.add(*distances)

load_tags(tags, Tag)
load_users(users, User, Tag)
load_distances(User, Distance)

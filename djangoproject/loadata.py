#python manage.py shell
#execfile('loadata.py')

from match.models import Profile, Tag, Distance

from utils.jsontools import read_json

profiles = read_json("utils/data/users.json")

tags = read_json("utils/data/tags.json")

#tanimoto
def tanimoto(u1, u2):
	"""
	u1, u2 are profile instances from a queryset
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

#Populate Profile table
def load_profiles(profiles, Profile, Tag):
	for profile, tags in profiles.iteritems():
		u = Profile.objects.create(name=profile)
		ts = []

		for tag in tags:
			t = Tag.objects.get(name=tag)
			ts.append(t)

		u.tags.add(*ts)

#Populate Distance table
def load_distances(Profile, Distance):
	profiles = Profile.objects.all()
	for from_profile in profiles:
		distances = []

		for to_profile in profiles:
			d = tanimoto(from_profile, to_profile)
			distance = Distance.objects.create(from_profile=from_profile, to_profile=to_profile, d=d)
			distances.append(distance)

		from_profile.distances.add(*distances)

load_tags(tags, Tag)
print "tags loaded"
load_profiles(profiles, Profile, Tag)
print "profiles loaded"
load_distances(Profile, Distance)
print "distances loaded"

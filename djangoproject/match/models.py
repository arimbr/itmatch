from django.db import models
from django import forms

from django.db.models.signals import * #selective import
from django.db.transaction import commit_on_success

# ------------ Utils ---------------------
# Import better

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
		return float(shr)/(c1 + c2 - shr)
	except ZeroDivisionError:
		return 0.0

# http://stackoverflow.com/questions/3395236/aggregating-saves-in-django
@commit_on_success
def load_distances(from_profile):
	profiles = Profile.objects.all()
	distances = []

	for to_profile in profiles:
		d = tanimoto(from_profile, to_profile)

		# from profile
		distance = Distance.objects.create(from_profile=from_profile, to_profile=to_profile, d=d)
		distances.append(distance)

		# to profile
		distance = Distance.objects.create(from_profile=to_profile, to_profile=from_profile, d=d)
		to_profile.distances.add(distance)

	from_profile.distances.add(*distances)


# ------------ Models --------------------

class Tag(models.Model):
	name = models.CharField(max_length=30)

	def __unicode__(self):
		return self.name

class Distance(models.Model):
	from_profile = models.ForeignKey('Profile', related_name = 'from_profile') # 'Profile' lets Django know that the reference may still be under construction.
	to_profile = models.ForeignKey('Profile', related_name = 'to_profile') #
	d = models.FloatField()

	def __unicode__(self):
		return "{0:.2f} to {1}".format(self.d, self.to_profile)

class Profile(models.Model):
	name = models.CharField(max_length=20) #unique=True
	tags = models.ManyToManyField('Tag', blank=True, null=True, related_name = 'profiles')
	distances = models.ManyToManyField('Distance', blank=True, null=True)

	def closer(self):
		#return self.distances.filter(d__lte=0.5).exclude(to_user=self).order_by('d')[:5]
		return self.distances.exclude(to_profile=self).filter(d__gt=0).order_by('d').reverse()[:5]

	def __unicode__(self):
		return self.name


# ------------- Forms --------------------------

#http://stackoverflow.com/questions/949268/django-accessing-the-model-instance-from-within-modeladmin
class ProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['tags'].queryset = self.instance.tags.all()
		self.fields['distances'].queryset = self.instance.distances.all().filter(d__gt=0).order_by('d')


# ------------- Signals ------------------------

def tags_changed(sender, **kwargs):
	if kwargs["action"] == "post_add":
		profile = kwargs["instance"]
		load_distances(profile)

m2m_changed.connect(tags_changed, sender=Profile.tags.through, weak=False)

#When changing models:
#python manage.py sqlclear match | python manage.py dbshell
#python manage.py syncdb

# CHECK south for django 1.6
# CHECK django migrations for django 1.7
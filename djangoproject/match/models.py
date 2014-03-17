from django.db import models
from django import forms

# Create your models here.

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
		return self.distances.exclude(to_profile=self).order_by('d')[:5]

	def __unicode__(self):
		return self.name


#http://stackoverflow.com/questions/949268/django-accessing-the-model-instance-from-within-modeladmin
class ProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['tags'].queryset = self.instance.tags.all()
		self.fields['distances'].queryset = self.instance.distances.all().filter(d__lt=1).order_by('d')

#When changing models:
#python manage.py sqlclear match | python manage.py dbshell
#Drop tables manually
#python manage.py syncdb
# CHECK south for django 1.6
# CHECK django migrations for django 1.7

#try sajjad.distances.all(), only shows with from_user = sajjad
#related_name = "distance_to", sajjad.distance_to.all() returns correct

#Bug admin shows all tags for each user - solved using forms. Can view but cannot edit properly

#Not sure that distances in User need to be recursive, instead ManyToManyField(Distancegq,...)
#Distance fields: to_user, distance (from_user = self)

#Rename attributes and add methods thinking of api lookups
#We want to call something like ari.distances.all().order_by("d")
#that returns an ordered list of profiles
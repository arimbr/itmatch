from django.db import models
from django import forms

# Create your models here.

class Tag(models.Model):
	name = models.CharField(max_length=30)

	def __unicode__(self):
		return self.name

class Distance(models.Model):
	from_user = models.ForeignKey('User', related_name = 'from_user') # 'User' lets Django know that the reference may still be under construction.
	to_user = models.ForeignKey('User', related_name = 'to_user') #
	d = models.FloatField()

	def __unicode__(self):
		return "{0} to {1}".format(self.from_user, self.to_user)

class User(models.Model):
	name = models.CharField(max_length=20)
	tags = models.ManyToManyField('Tag' related_name="users")
	distances = models.ManyToManyField('Distance')

	def __unicode__(self):
		return self.name

#http://stackoverflow.com/questions/949268/django-accessing-the-model-instance-from-within-modeladmin
class UserForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['tags'].queryset = self.instance.tags.all()
		self.fields['distances'].queryset = self.instance.distances.all()

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
#that returns an ordered list of users
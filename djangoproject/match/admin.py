from django.contrib import admin
from match.models import Profile, Tag, Distance, ProfileForm

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
	#filter_horizontal = ('tags',)
	form = ProfileForm

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag)

#bug admin when adding tag manually from user profile it adds it to everyone
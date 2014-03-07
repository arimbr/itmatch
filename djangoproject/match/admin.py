from django.contrib import admin
from match.models import User, Tag, Distance, UserForm

# Register your models here.

class UserAdmin(admin.ModelAdmin):
	#filter_horizontal = ('tags',)
	form = UserForm

admin.site.register(User, UserAdmin)
admin.site.register(Tag)

#bug admin when adding tag manually from user profile it adds it to everyone
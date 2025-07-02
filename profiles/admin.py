from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)

# This code registers the Profile model with the Django admin site, allowing it to be managed through the admin interface.
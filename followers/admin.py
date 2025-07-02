from django.contrib import admin
from .models import Follower

# Register your models here.

class FollowerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Follower, FollowerAdmin)
# This code registers the Post model with the Django admin site, allowing it to be managed through the admin interface.
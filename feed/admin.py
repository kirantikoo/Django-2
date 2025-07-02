from django.contrib import admin
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    list_filter = ('date',)
# This code registers the Post model with the Django admin site, allowing it to be managed through the admin interface.
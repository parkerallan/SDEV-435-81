# Description: Admin portal configuration for posts app
# The Post and Comment models and their attributes are registered with the admin site which allows the admin to manage them in the portal
# The admin can view, create, update, and delete posts and comments. Very useful for managing the content and debugging issues
# The admin portal is accessible at /admin/ and requires superuser account

from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at', 'total_likes', 'total_dislikes')
    search_fields = ('content', 'author__username')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_at')
    search_fields = ('content', 'author__username', 'post__content')
    list_filter = ('created_at',)
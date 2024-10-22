from django.shortcuts import get_object_or_404
from .models import Post, Activity

def like_dislike(request, post_id):
    """Handles the like and dislike logic for a post."""
    post = get_object_or_404(Post, id=post_id)
    action = request.POST.get('action')
    Activity.objects.create(user=request.user, action=action, post=post)

    if action == 'like':
        if request.user in post.likes.all():
            post.likes.remove(request.user)  # Remove like
        else:
            post.likes.add(request.user)      # Add like
            post.dislikes.remove(request.user)  # Remove dislike if exists

    elif action == 'dislike':
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)  # Remove dislike
        else:
            post.dislikes.add(request.user)      # Add dislike
            post.likes.remove(request.user)      # Remove like if exists

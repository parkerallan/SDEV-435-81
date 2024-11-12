# Description: This file contains the resusable functions for the post's app view.
# The only utility functions used is to handle the like and dislike logic for a post.

from django.shortcuts import get_object_or_404
from .models import Post, Activity

def like_dislike(request, post_id):
    post = get_object_or_404(Post, id=post_id)                              # Get the post object by ID
    action = request.POST.get('action')                                     # Get the action if it's like/dislike
    Activity.objects.create(user=request.user, action=action, post=post)    # Create a new activity for the like/dislike

    # Conditional logic for whether the user has liked or disliked the post and clicks the button again
    if action == 'like':
        if request.user in post.likes.all():                                # Check if the user has already liked the post
            post.likes.remove(request.user)                                 # Remove like
        else:
            post.likes.add(request.user)                                    # Add like
            post.dislikes.remove(request.user)                              # Remove dislike if exists

    elif action == 'dislike':
        if request.user in post.dislikes.all():                             # Check if the user has already disliked the post
            post.dislikes.remove(request.user)                              # Remove dislike
        else:
            post.dislikes.add(request.user)                                 # Add dislike
            post.likes.remove(request.user)                                 # Remove like if exists

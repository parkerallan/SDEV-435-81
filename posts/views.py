# Description: This file contains the views for the posts app.
# The views are used to render the templates for the posts app.
# The views also handle the logic for creating, updating, and deleting posts and comments.
# The views also call the logic for liking and disliking posts, function is in utils.py

from django.shortcuts import render, get_object_or_404, redirect    # Import the render, get_object_or_404, and redirect functions
from django.contrib.auth.decorators import login_required           # Import the login_required decorator
from .models import Post, Comment, Activity                         # Import the Post, Comment, and Activity models
from django.contrib import messages
from .utils import like_dislike                                     # Import the like_dislike function from utils.py

@login_required(login_url='/login/')                        # Ensure the user is logged in otherwise redirect to the login page
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')      # Get all posts and order them by the created_at field
    
    if request.method == 'POST':                            # Check if the request method is POST
        post_id = request.POST.get('post_id')               # Get the post ID
        action = request.POST.get('action')                 # Get the action if it's like/dislike
        post = get_object_or_404(Post, id=post_id)          # Get the post object

        # Handle like and dislike actions
        if 'action' in request.POST:                        # Check if the action is like/dislike
            like_dislike(request, post_id)                  # Call the like_dislike function from utils.py
                
        elif 'content' in request.POST:                     # Check if the content is in the request
            comment_content = request.POST.get('content')   # Get the comment content
            if comment_content.strip():                     # Ensure the comment isn't empty
                Comment.objects.create(post=post, author=request.user, content=comment_content)     # Create a new comment
                Activity.objects.create(user=request.user, action='comment', post=post)             # Create a new activity for the comment

        return redirect('feed')                             # Redirect to the feed view
    
    return render(request, 'feed.html', {'posts': posts})   # Finally, render the feed.html template with the posts data

@login_required(login_url='/login/')
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)                   # Get the post object by ID

    if request.method == 'POST':                            # Check if the request method is POST
        action = request.POST.get('action')                 # Get the action if it's like/dislike
        post_id = request.POST.get('post_id')               # Get the post ID
        comment_content = request.POST.get('content')       # Get the comment content

        # Handle like and dislike actions
        if 'action' in request.POST:
            like_dislike(request, post_id)

        # Handle comment submission
        if comment_content and post_id:                     # Check if content and post ID are available
            if comment_content.strip():                     # Ensure the comment isn't empty
                Comment.objects.create(post=post, author=request.user, content=comment_content)
                Activity.objects.create(user=request.user, action='comment', post=post)

        return redirect('post_detail', id=post.id)              # Redirect to the post detail view by the post ID

    return render(request, 'post_detail.html', {'post': post})  # Render the post_detail.html template with the post data

@login_required(login_url='/login/')
def create_post(request):
    if request.method == 'POST':                                                            # Check if the request method is POST
        content = request.POST.get('content')                                               # Get the content from the request
        post = Post.objects.create(author=request.user, content=content)                    # Create a new post
        activities = Activity.objects.create(user=request.user, action='post', post=post)   # Create a new activity for the post
        return redirect('feed')                                                             # Redirect to the feed view
    return render(request, 'create_post.html')                                              # Render the create_post.html template

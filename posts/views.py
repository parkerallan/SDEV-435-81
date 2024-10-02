from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib import messages
from .utils import like_dislike

@login_required(login_url='/login/')
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        post = get_object_or_404(Post, id=post_id)

        # Handle like and dislike actions
        if 'action' in request.POST:
            like_dislike(request, post_id)
                
        elif 'content' in request.POST:
            comment_content = request.POST.get('content')
            if comment_content.strip():  # Ensure the comment isn't empty
                Comment.objects.create(post=post, author=request.user, content=comment_content)

        return redirect('feed')
    
    return render(request, 'feed.html', {'posts': posts})

@login_required(login_url='/login/')
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')  # Get the action if it's like/dislike
        post_id = request.POST.get('post_id')  # Get the post ID
        comment_content = request.POST.get('content')  # Get the comment content

        # Handle like and dislike actions
        if 'action' in request.POST:
            like_dislike(request, post_id)

        # Handle comment submission
        if comment_content and post_id:  # Check if content and post ID are available
            if comment_content.strip():  # Ensure the comment isn't empty
                Comment.objects.create(post=post, author=request.user, content=comment_content)

        return redirect('post_detail', pk=post.pk)  # Redirect to the post detail view

    return render(request, 'post_detail.html', {'post': post})

@login_required(login_url='/login/')
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(author=request.user, content=content)
        return redirect('feed')
    return render(request, 'create_post.html')

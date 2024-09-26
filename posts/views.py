from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib import messages

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        post = get_object_or_404(Post, id=post_id)

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
        comment_content = request.POST.get('content')
        Comment.objects.create(post=post, author=request.user, content=comment_content)
        return redirect('post_detail', pk=post.pk)
    return render(request, 'post_detail.html', {'post': post})

@login_required(login_url='/login/')
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(author=request.user, content=content)
        return redirect('feed')
    return render(request, 'create_post.html')

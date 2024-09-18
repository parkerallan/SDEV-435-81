from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib import messages

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment_content = request.POST.get('content')
        Comment.objects.create(post=post, author=request.user, content=comment_content)
        messages.success(request, 'Your comment has been posted!')
        return redirect('post_detail', pk=post.pk)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(author=request.user, content=content)
        messages.success(request, 'Your post has been created!')
        return redirect('post_list')
    return render(request, 'posts/create_post.html')

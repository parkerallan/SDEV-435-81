from django.db import models
from django.contrib.auth.models import User
import uuid

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()
    
    def total_comments(self):
        return self.comments.count()

    def __str__(self):
        return f'Post by {self.author.username}'

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'

class Activity(models.Model):
    ACTION_CHOICES = (
        ('post', 'Post Created'),
        ('comment', 'Commented'),
        ('like', 'Liked')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    target_user = models.ForeignKey(User, related_name='target_user', on_delete=models.SET_NULL, null=True)  # might remove
    post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True)  # Linking to a post 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.action} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
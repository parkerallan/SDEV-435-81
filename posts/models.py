# Description: This file contains the models for the posts app. The models define the structure of the database tables.
# The model have fields for the associated attributes of the post, comment, and activity actions.
# The models define relationships between the users and their posts, comments, and activities.
# The models also defines the data types for the fields in the database tables. (e.g., CharField, TextField, DateTimeField)

from django.db import models
from django.contrib.auth.models import User
import uuid                                                                             # Required for unique post IDs

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)         # Unique ID for the post
    author = models.ForeignKey(User, on_delete=models.CASCADE)                          # Linking to the user who created the post
    content = models.TextField()                                                        # Content of the post
    created_at = models.DateTimeField(auto_now_add=True)                                # Date and time when the post was created
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)         # Users who liked the post
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)   # Users who disliked the post

    def total_likes(self):                                                              # Method to get the total likes on a post
        return self.likes.count()

    def total_dislikes(self):                                                           # Method to get the total dislikes on a post
        return self.dislikes.count()
    
    def total_comments(self):                                                           # Method to get the total comments on a post
        return self.comments.count()

    def __str__(self):
        return f'Post by {self.author.username}'

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)   # Linking to the post
    author = models.ForeignKey(User, on_delete=models.CASCADE)                          # Linking to the user who created the comment
    content = models.TextField()                                                        # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True)                                # Date and time when the comment was created

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'

class Activity(models.Model):
    ACTION_CHOICES = (                                                                                          # Defining the choices for the action field
        ('post', 'Post Created'),
        ('comment', 'Commented'),
        ('like', 'Liked')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)                                                    # Linking to the user who performed the action
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)                                            # Action performed by the user
    target_user = models.ForeignKey(User, related_name='target_user', on_delete=models.SET_NULL, null=True)     # Linking to the target user (not used)
    post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True)                          # Linking to a post 
    created_at = models.DateTimeField(auto_now_add=True)                                                        # Date and time when the action was performed

    def __str__(self):
        return f"{self.user.username} {self.action} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"         # Return the user, action, and created_at fields
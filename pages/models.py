# Description: This file contains the Profile model which is used to store additional information about the user.
# The Profile model is linked to the User model using a OneToOneField, which ensures that each user has only one profile.
# The Profile model contains fields for display name, bio, and social links.

from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Add a UUID field as the primary key
    user = models.OneToOneField(User, on_delete=models.CASCADE)                 # Link the Profile model to the User model using a OneToOneField
    display_name = models.CharField(max_length=100, blank=True)                 # Add a field for the display name
    bio = models.TextField(blank=True)                                          # Add a field for the bio
    social_links = models.URLField(blank=True, null=True)                       # Add a field for social links

    def __str__(self):
        return f'{self.user.username} Profile'

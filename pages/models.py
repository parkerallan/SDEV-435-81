from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    social_links = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

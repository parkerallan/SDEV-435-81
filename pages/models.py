from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    social_links = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

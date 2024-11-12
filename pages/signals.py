# Description: This file is used to create or save a profile for each user that is created.
# This is done by creating a signal that listens for when a user is created or saved.

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)           # Create a profile for the user

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()                             # Save the profile for the user

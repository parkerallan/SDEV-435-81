# Description: This file contains the URL patterns for the Posts app.
# The URL patterns are defined using the path() function which takes in the URL pattern and the view function.
# The URL patterns are used to direct the user to the correct view function based on the URL path.
# We call the view function with the correct URL pattern and the view function returns the correct HTML page.
# The name parameter is used to give the URL pattern a name which can be used to refer to the URL pattern in the Django templates.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import post_detail, create_post # Import the post_detail and create_post view functions from this app's views.py file

urlpatterns = [
    path('<uuid:id>/', post_detail, name='post_detail'), # Add a route to view a post by passing in the post's id value (uuid)
    path('create/', create_post, name='create_post'), # Add a route to create a new post
]

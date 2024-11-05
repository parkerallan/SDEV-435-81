# Description: This file contains the URL patterns for Posts and more general routes of social_media_app.
# The URL patterns are defined using the path() function which takes in the URL pattern and the view function.
# The URL patterns are used to direct the user to the correct view function based on the URL path.
# We call the view function with the correct URL pattern and the view function returns the correct HTML page.
# The name parameter is used to give the URL pattern a name which can be used to refer to the URL pattern in the Django templates.

from django.contrib import admin # Import the admin module which is used to create the admin page
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pages.views import * # Import all view functions from pages.views
from posts.views import * # Import all view functions from posts.views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'), # Open admin page route using admin.site.urls
    path('', home_view, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('about/', about_view, name='about'),
    path('contact/', redirect_to_website, name='contact'),
    
    path('feed/', post_list, name='feed'),
    path('posts/', include('posts.urls')),
    
    path('register/', register_view, name='register'),
    path('registered/', registered_view, name='registered'),
    
    path('myprofile/', my_profile, name='myprofile'),
    path('userprofile/<uuid:id>/', user_profile, name='userprofile') # Add a route to view a user's profile by passing in the user's id value (uuid)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Add the media URL and document root to urlpatterns if DEBUG is True
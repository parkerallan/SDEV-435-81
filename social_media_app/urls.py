from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pages.views import *
from posts.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', home_view, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('about/', about_view, name='about'),
    path('contact/', redirect_to_website, name='contact'),
    
    path('feed/', post_list, name='feed'),
    path('posts/', include('posts.urls')),
    
    path('register/', register_view, name='register'),
    path('registered/', registered_view, name='registered'),
    
    path('myprofile/', my_profile, name='myprofile'),
    path('userprofile/<uuid:id>/', user_profile, name='userprofile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
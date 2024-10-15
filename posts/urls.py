from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import post_detail, create_post

urlpatterns = [
    path('<uuid:id>/', post_detail, name='post_detail'),
    path('create/', create_post, name='create_post'),
]

# Description: This file is used to configure the ASGI application for the project.
# The ASGI application is used to handle asynchronous requests in Django in a production environment.
# The application variable is used to define the ASGI application for the project.
# For a small project like this, ASGI concurrency is not required.
# I am not using the ASGI application in this project, instead I'm using the WSGI application instead.

"""
ASGI config for social_media_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_app.settings')

application = get_asgi_application()

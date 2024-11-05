# Description: This file is used to configure the WSGI application for the project.
# The WSGI application is used to handle synchronous requests in Django in a production environment.
# The application variable is used to define the WSGI application for the project.
# WSGI offers the most flexibility with web servers and is the most commonly used deployment method for Django projects.
# I am using the WSGI application in this project.

"""
WSGI config for social_media_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_app.settings')

application = get_wsgi_application()

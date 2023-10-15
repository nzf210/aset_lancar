"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "main.settings"
aplication = get_wsgi_application()
app = aplication

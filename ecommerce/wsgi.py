"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

ENVIRONMENT = os.environ.get("ENV")
if ENVIRONMENT == "dev":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings.dev')
elif ENVIRONMENT == "prod":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings.prod')
else:
    print("-> Missing ENV variable (dev | prod)")
    sys.exit(1)

application = get_wsgi_application()

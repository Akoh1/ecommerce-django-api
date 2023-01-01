from .base import *
from decouple import config

DEBUG = True

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = []
# CSRF_HEADER_NAME = "X_CSRFTOKEN"
# CSRF_COOKIE_NAME = "XSRF-TOKEN"
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS_ALLOW_HEADERS = "*"
# CORS_ORIGIN_WHITELIST = [
#     'http://127.0.0.1:3000',
#     'http://localhost:3000'
# ]

# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_HEADERS = [
#     "accept",
#     "accept-encoding",
#     "authorization",
#     "content-type",
#     "content-disposition",
#     "dnt",
#     "origin",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
# ]
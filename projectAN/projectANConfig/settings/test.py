import os
from ._base import *
from django.core.exceptions import ImproperlyConfigured
    
STATE =  os.getenv("STATE")
SECRET_KEY = os.getenv("SECRET_KEY")
GOOGLE_OAUTH2_CLIENT_ID = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")

DEBUG = True

# add host ip
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = ['http://54.180.118.117:3000']

WSGI_APPLICATION = 'projectANConfig.wsgi.test.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
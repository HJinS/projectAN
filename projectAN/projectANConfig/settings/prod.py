import os
from ._base import *
    
STATE =  os.getenv("STATE")
SECRET_KEY = os.getenv("SECRET_KEY")
GOOGLE_OAUTH2_CLIENT_ID = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")

DEBUG = False

# add host ip
ALLOWED_HOSTS = []

WSGI_APPLICATION = 'projectANConfig.wsgi.prod.application'

CORS_ORIGIN_WHITELIST = ['*']

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    },
}
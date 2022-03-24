import os, json
from ._base import *
from django.core.exceptions import ImproperlyConfigured

def __get_secret(key):
    secret_path = os.path.join(BASE_DIR, 'secrets.json')
    with open(secret_path) as file:
        secrets = json.loads(file.read())
    try:
        return secrets[key]
    except KeyError:
        error_message = "Set the {} environment variable".format(key)
        raise ImproperlyConfigured(error_message)
    
STATE =  __get_secret("STATE")
SECRET_KEY = __get_secret("SECRET_KEY")
GOOGLE_OAUTH2_CLIENT_ID = __get_secret("GOOGLE_OAUTH2_CLIENT_ID")
GOOGLE_OAUTH2_CLIENT_SECRET = __get_secret("GOOGLE_OAUTH2_CLIENT_SECRET")

DEBUG = True

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8000',
    'http://localhost:3000',
]

ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'projectANConfig.wsgi.dev.application'

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'an',
        'USER': __get_secret('DB_USER'),
        'PASSWORD': __get_secret('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

BASE_URL = __get_secret("BASE_URL")
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

CORS_ALLOWED_ORIGINS = [
    'http://3.39.71.147',
    'http://localhost',
    'http://3.39.71.147:5000',
    'http://3.39.71.147:8000',
    'https://accounts.google.com'
]
CORS_ALLOW_CREDENTIALS = True
WSGI_APPLICATION = 'projectANConfig.wsgi.test.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_jslint',
    'django_jenkins.tasks.run_csslint',    
    'django_jenkins.tasks.run_sloccount'
)

BASE_URL = os.getenv("BASE_URL")
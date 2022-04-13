import os
from ._base import *
    
STATE =  os.getenv("STATE")
SECRET_KEY = os.getenv("SECRET_KEY")
GOOGLE_OAUTH2_CLIENT_ID = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")

DEBUG = False

# add host ip
ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'projectANConfig.wsgi.prod.application'

CORS_ALLOWED_ORIGINS = [
    'http://3.39.71.147',
    'http://localhost',
    'http://3.39.71.147:5000',
    'http://3.39.71.147:8000',
    'https://accounts.google.com'
]

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    },
}

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_jslint',
    'django_jenkins.tasks.run_csslint',    
    'django_jenkins.tasks.run_sloccount'
)

BASE_URL = os.getenv("BASE_URL")
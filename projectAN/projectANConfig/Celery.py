from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectANConfig.settings')
#HOST = os.environ.get('SERVER_HOST')
app = Celery('projectAN', broker=f'amqp://guest:guest@localhost//')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
if not DJANGO_SETTINGS_MODULE:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectANConfig.settings.dev')
elif DJANGO_SETTINGS_MODULE == 'projectANConfig.settings.prod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectANConfig.settings.prod')
elif DJANGO_SETTINGS_MODULE == 'projectANConfig.settings.test':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectANConfig.settings.test')

app = Celery('projectAN_Celery', broker='amqp://guest:guest@rabbitmq//', include=['projectANConfig.celery_space.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
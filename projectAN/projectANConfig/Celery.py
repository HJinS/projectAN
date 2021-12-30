from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectANConfig.settings')

app = Celery('projectAN', broker='amqp://guest:guest@localhost:5672//')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.update(
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TIMEZONE = 'Asia/Seoul',
    CELERY_ENABLE_UTC = False,
    CELERYBEAT_SCHEDULE = {
        'say_hello-every-seconds' : {
            "task" : "AN.tasks.say_hello",
            'schedule' : timedelta(seconds=30),
            'args' : ()
        }
    }
)
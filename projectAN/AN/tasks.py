from __future__ import absolute_import

from projectANConfig.Celery import app

@app.task
def say_hello():
    print("hello world")
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bbgraph.settings')

app = Celery('bbgraph',
             broker='redis://redis:6379/',
             backend='redis://redis:6379/',
             include=['grapher.tasks'])

app.conf.update(result_expires=3600,)
app.conf.timezone = 'Europe/London'
app.conf.update(
     CELERY_ACCEPT_CONTENT = ['json'],
     CELERY_TASK_SERIALIZER = 'json',
     CELERY_RESULT_SERIALIZER = 'json',
)
# app.conf.broker_url = 'amqp://localhost:6379/0'
# app.conf.result_backend = 'redis://localhost:6379/0'
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()

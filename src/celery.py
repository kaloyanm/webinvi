from __future__ import absolute_import, unicode_literals
import os
import logging
from celery import Celery
from raven import Client
from raven.contrib.celery import register_signal, register_logger_signal


# Setup raven/sentry
client = Client(os.environ.get("SENTRY_DSN"))

# register a custom filter to filter out duplicate logs
register_logger_signal(client)

# The register_logger_signal function can also take an optional argument
# `loglevel` which is the level used for the handler created.
# Defaults to `logging.ERROR`
register_logger_signal(client, loglevel=logging.INFO)

# hook into the Celery error handler
register_signal(client)

# The register_signal function can also take an optional argument
# `ignore_expected` which causes exception classes specified in Task.throws
# to be ignored
register_signal(client, ignore_expected=True)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = Celery('invoiceapp')
app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
    'search-vector-every-10-minutes': {
        'task': 'invoices.tasks.update_search_vector',
        'schedule': 60 * 10,
        'args': [],
    }
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    raise Exception('Hello from celery')
    print('Request: {0!r}'.format(self.request))

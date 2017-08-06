
import logging
import os

from unittest import mock
from django.shortcuts import render

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.src.settings'
os.environ['DEBUG'] = 'False'


def render_wrapper(request, template_name, context=None, *args, **kwargs):
    response = render(request, template_name, context, *args, **kwargs)
    response.context = context
    response.template_name = template_name
    return response


def pytest_configure(config):
    logging.getLogger('django.db.backends.schema').setLevel(logging.INFO)
    mock.patch('django.shortcuts.render', render_wrapper).start()

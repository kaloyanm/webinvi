import requests
from celery import task
from django.contrib.postgres.search import SearchVector
from invoices.models import Invoice


@task
def update_search_vector():
    vector = SearchVector('client_name') + SearchVector('client_city')
    vector += SearchVector('client_mol') + SearchVector('client_address')

    for inv in Invoice.objects.annotate(document=vector):
        inv.search_vector = inv.document
        inv.save(update_fields=['search_vector'])

from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    name = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    mol = models.CharField(max_length=255, default='')
    eik = models.CharField(max_length=255)
    dds = models.CharField(max_length=255, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    payment_iban = models.CharField(max_length=255, null=True)
    payment_swift = models.CharField(max_length=255, null=True)
    payment_type = models.CharField(max_length=155, null=True)
    payment_bank = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.eik)

    def get_absolute_url(self):
        return reverse('company', args=[self.pk])

    @property
    def has_invoices(self):
        return self.invoice_set.count() > 0


def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        Company.objects.create(user=instance)
post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)


from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from oauth2client.contrib.django_util.models import CredentialsField
from core.mixins import FillEmptyTranslationsMixin


# Create your models here.
class Company(FillEmptyTranslationsMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, default='')
    name_tr = models.CharField(max_length=255, null=True)

    city = models.CharField(max_length=255, default='')
    city_tr = models.CharField(max_length=255, null=True)

    address = models.CharField(max_length=255, default='')
    address_tr = models.CharField(max_length=255, null=True)

    mol = models.CharField(max_length=255, default='')
    mol_tr = models.CharField(max_length=255, null=True)

    eik = models.CharField(max_length=255)
    dds = models.CharField(max_length=255, null=True, blank=True)

    last_updated = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.eik)

    def get_absolute_url(self):
        return reverse('company', args=[self.pk])

    @property
    def delete_url(self):
        return reverse('drop_company', args=[self.pk])

    @property
    def has_invoices(self):
        return self.invoice_set.count() > 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.default:
            Company.objects.filter(user=self.user).exclude(pk=self.pk).update(default=False)
        elif not Company.objects.filter(user=self.user, default=True).exists():
            Company.objects.filter(pk=self.pk).update(default=True)


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    gdrive_sync = models.BooleanField(default=False)


def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)


post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()


class CredentialsAdmin(admin.ModelAdmin):
    pass

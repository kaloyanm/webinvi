from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User)

    # Company details
    provider_name = models.CharField(max_length=255)
    provider_eik = models.CharField(max_length=255)
    provider_dds = models.CharField(max_length=255, blank=True)
    provider_city = models.CharField(max_length=255)
    provider_address = models.CharField(max_length=255)
    provider_mol = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.provider_name, self.provider_eik)
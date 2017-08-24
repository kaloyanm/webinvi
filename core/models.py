
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    eik = models.CharField(max_length=255, unique=True)
    dds = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    mol = models.CharField(max_length=255)
    default = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return "{} ({})".format(self.name, self.eik)

    def get_absolute_url(self):
        return reverse('core.views.company', args=[self.pk])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.default:
            Company.objects.filter(user=self.user).exclude(pk=self.pk).update(default=False)
        elif not Company.objects.filter(user=self.user, default=True).exists():
            Company.objects.filter(pk=self.pk).update(default=True)


class CompanyAccess(models.Model):

    company = models.ForeignKey(Company)
    user = models.ForeignKey(User, null=True)
    email = models.EmailField(db_index=True)
    verified = models.BooleanField(default=False)
    invitation_key = models.CharField(max_length=155, db_index=True)
    expire_on = models.DateField()

    class Meta:
        unique_together = ("company", "user")

    def __str__(self):
        return str(_("Точка за достъп на {} за {}".format(self.email, self.company)))

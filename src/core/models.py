from django.db import models
from django.contrib.auth.models import User


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

    class Meta:
        unique_together = ('default', 'user')

    def __str__(self):
        return "{} ({})".format(self.name, self.eik)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.default:
            Company.objects.filter(user=self.user).exclude(pk=self.pk).update(default=False)

    @staticmethod
    def get_default(user):
        return

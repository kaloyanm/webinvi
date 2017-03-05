from django.db import models


# Create your models here.
class ExchangeRate(models.Model):
    pass


class ExchangeCurrency(models.Model):
    short_code = models.CharField(max_length=5)
    long_code = models.CharField(max_length=155)

from __future__ import unicode_literals

from django.db import models
from stores.models import Store


class Stock(models.Model):
    """
    Stocks on items
    """
    store = models.ForeignKey(Store)
    description = models.TextField()
    new_price = models.IntegerField()
    end_time = models.DateField()

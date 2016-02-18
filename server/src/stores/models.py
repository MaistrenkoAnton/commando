from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from catalogue.models import Item

# Create your models here.


class Store(models.Model):
    class Meta:
        db_table = "sites"
        ordering = ["title"]
        verbose_name = "site"
        verbose_name_plural = "sites"

    title = models.CharField(max_length=100)
    margin = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    activity_status = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("stores:store", kwargs={"pk": self.id, })

    def __unicode__(self):
        return self.title


class StoreItem(Item):

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=True)
    running_out_level = models.IntegerField(default=10, blank=True)

    @property
    def running_out(self):
        """
        Function returns True if quantity of items in stock is less or equal to running out level set
        """
        return self.quantity <= self.running_out_level

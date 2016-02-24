from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse


class Store(models.Model):
    # class Meta:
    #     db_table = "stores"
    #     ordering = ["title"]
    #     verbose_name = "store"
    #     verbose_name_plural = "stores"

    title = models.CharField(max_length=100)
    margin = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    activity_status = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("stores:store", kwargs={"pk": self.id, })

    def __unicode__(self):
        return self.title

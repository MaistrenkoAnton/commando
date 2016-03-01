from __future__ import unicode_literals
from django.contrib.auth.models import User
from catalogue.models import Item
from django.db import models


class Cart(models.Model):
    """
    Model for cart
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item)
    purchase_time = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()

    def __unicode__(self):
        return u'{user} / {item}'.format(user=self.user, item=self.item)


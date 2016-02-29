from .models import Item
from stock.models import Stock
from django.db.models.signals import post_delete, post_save
from .jobs import ItemJob
from django.dispatch import receiver
invalidate_signals = [post_delete, post_save]


@receiver(invalidate_signals, sender=Item)
def invalidate_item(sender, instance, **kwargs):
    ItemJob().invalidate(pk=str(instance.pk))


@receiver(invalidate_signals, sender=Stock)
def invalidate_stock(sender, instance, **kwargs):
    ItemJob().invalidate(pk=str(instance.pk))
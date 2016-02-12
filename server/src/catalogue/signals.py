from .models import Item, Category
from django.db.models.signals import post_delete, post_save
from .jobs import ItemJob, CategoryListJob
from django.dispatch import receiver
invalidate_signals = [post_delete, post_save]


@receiver(invalidate_signals, sender=Item)
def invalidate_item(sender, instance, **kwargs):
    print('invalidate item')
    ItemJob().invalidate(pk=str(instance.pk))


@receiver(invalidate_signals, sender=Category)
def invalidate_category(sender, instance, **kwargs):
    print('invalidate category')
    CategoryListJob().invalidate(instance.parent)

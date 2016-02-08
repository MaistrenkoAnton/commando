from django.db import models
import mptt


class Category(models.Model):
    """
    Category of products and subcategories
    """
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Item(models.Model):
    """
    Item of product
    """
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.ForeignKey(Category)
    rate = models.IntegerField()


mptt.register(Category, )


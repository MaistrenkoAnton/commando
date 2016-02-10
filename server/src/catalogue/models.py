from django.db import models
import mptt
from django.core.urlresolvers import reverse


class Category(models.Model):
    """
    Category of products
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
    image_url = models.ImageField(blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category)

    def get_absolute_url(self):
        return reverse("itemdetail", kwargs={"pk": self.id, })

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

mptt.register(Category, )

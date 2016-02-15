from django.db import models
import mptt
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


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
    average_rate = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    comments_total = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("itemdetail", kwargs={"pk": self.id, })

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

mptt.register(Category, )


class Comment(models.Model):
    """
    Comments for items
    """
    text = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, blank=False, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'{l}, {f}'.format(l="Comment No.", f=self.id)


class RateSet(models.Model):
    """
    Flag to show if rate for defined item by defined user is set
    """
    rate_is_set = models.BooleanField(default=True)
    item = models.OneToOneField(Item, blank=False, null=False, on_delete=models.CASCADE)
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'{l}, {f}'.format(l="Rate No.", f=self.id)

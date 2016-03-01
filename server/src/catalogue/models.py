from django.db import models
import mptt
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from stores.models import Store
from stock.models import Stock


class Category(models.Model):
    """
    Category of products
    """
    class Meta:
        db_table = "categories"
        verbose_name = "category"
        verbose_name_plural = "categories"

    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

mptt.register(Category, )


class Item(models.Model):
    """
    Item of product
    """
    class Meta:
        db_table = "items"
        verbose_name = "item"
        verbose_name_plural = "items"
        ordering = ["price"]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False)
    image_url = models.ImageField(blank=True, default='/static/images.jpg')
    description = models.TextField()
    category = models.ForeignKey(Category)
    average_rate = models.DecimalField(max_digits=6, decimal_places=5, default=0.0)
    rates_total = models.IntegerField(default=0)
    rates = models.ManyToManyField(User, related_name="rates", through="Rate")
    comments_total = models.IntegerField(default=0)
    comments = models.ManyToManyField(User, related_name="comments", through="Comment")
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=True)
    running_out_level = models.IntegerField(default=10, blank=True)
    stock = models.ForeignKey(Stock, blank=True, null=True)

    @property
    def running_out(self):
        """
        Returns True if quantity of items in stock is less or equal to running out level set
        """
        return self.quantity <= self.running_out_level

    def get_absolute_url(self):
        return reverse("itemdetail", kwargs={"pk": self.id, })

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    """
    Comments for items
    """
    class Meta:
        db_table = "comment"
        verbose_name = "comment"
        verbose_name_plural = "comments"

    text = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, blank=False, null=False, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        """
        Increment 'comments_total' field of the Item object on every comment added so, that this field always shows
        actual number of existing comments, related to this Item object
        """
        self.item.comments_total += 1
        self.item.save()
        super(Comment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Decrement 'comments_total' field of the Item object on every comment added so, that this field always shows
        actual number of existing comments, related to this Item object
        """
        self.item.comments_total -= 1
        self.item.save()
        super(Comment, self).delete(*args, **kwargs)

    def __unicode__(self):
        return u'{item} / {author}'.format(item=self.item, author=self.author)


class Rate(models.Model):
    """
    Flag to show if rate for defined item by defined user is set
    """
    rate = models.IntegerField(blank=False, null=False)
    item = models.ForeignKey(Item, blank=False, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("item", "user"),)

    def save(self, *args, **kwargs):
        """
        Increment 'rates_total' field and set new value to 'average_rate' field of the Item object every time new rate
        is set
        """
        self.item.rates_total += 1
        self.item.average_rate += (self.item.average_rate + self.rate) / self.item.rates_total
        self.item.save()
        super(Rate, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{item} / {user}'.format(item=self.item, user=self.user)

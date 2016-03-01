from __future__ import unicode_literals
from django.utils import timezone
from django.core.validators import ValidationError
from django.db import models
from stores.models import Store


class Stock(models.Model):
    """
    Model for stocks
    """
    class Meta:
        db_table = "stocks"
        ordering = ["title"]
        verbose_name = "stock"
        verbose_name_plural = "stocks"

    title = models.CharField(max_length=150)
    store = models.ForeignKey(Store)
    description = models.TextField()
    discount = models.IntegerField()
    start = models.DateField(default=timezone.now())
    finish = models.DateField()

    def save(self, *args, **kwargs):
        """
        Prevent setting 'Finish' date in the past in relation to the 'Start' date.
        """
        if self.start > self.finish:
            raise ValidationError("'Finish' date can not be set in the past in relation to the 'Start' date.")
        super(Stock, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category)


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    subcategory = models.ForeignKey(Subcategory)


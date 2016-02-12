from rest_framework.response import Response
from rest_framework import generics
from .models import Item, Category
from .serializers import (ItemListSerializer, CategoryListSerializer,
                          CategoryAddSerializer, ItemDetailSerializer,
                          ItemAddSerializer)
from rest_framework.views import APIView
from cacheback.base import Job
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
invalidate_signals = [post_delete, post_save]


@receiver(invalidate_signals, sender=Item)
def invalidate_item(sender, instance, **kwargs):
    ItemJob().invalidate(instance.pk)


@receiver(invalidate_signals, sender=Category)
def invalidate_category(sender, instance, **kwargs):
    print('invalidate_Cat')
    CategoryListJob().invalidate(instance.parent)


class ItemJob(Job):
    """
    Send and get detail info item cache
    """
    def fetch(self, pk):
        item = ItemDetailSerializer(Item.objects.get(pk=pk)).data
        return item


class CategoryListJob(Job):
    """
    Send and get list categories into cache
    """
    def fetch(self, pk=None):
        category_list = CategoryListSerializer(Category.objects.filter(parent=pk), many=True).data
        return category_list


class ItemDetailView(APIView):
    """
    Get Detail Item by pk
    pk -- particular item's id
    """
    def get(self, request, pk):
        item1 = ItemJob().get(pk)
        return Response(item1)


class CategoryListView(APIView):
    """
    Category List
    pk -- filter by primary key
    """
    def get(self, request, pk=None):
        category_response = CategoryListJob().get(pk)
        return Response(category_response)


class ItemListView(APIView):
    """
    List Items
    pk -- filter by category
    """
    serializer = ItemListSerializer
    model = Item

    def get(self, request, pk):
        response_data = self.serializer(self._get_queryset(pk), many=True).data
        return Response(response_data)

    def _get_queryset(self, pk):
        return self.model.objects.filter(category=pk).order_by('price')


class ItemAddView(generics.CreateAPIView):
    """
    Add Item
    """
    queryset = Item.objects.all()
    serializer_class = ItemAddSerializer


class CategoryAddView(generics.CreateAPIView):
    """
    Add category
    """
    queryset = Category.objects.all()
    serializer_class = CategoryAddSerializer

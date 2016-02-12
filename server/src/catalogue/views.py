from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework import generics
from .models import Item, Category
from .serializers import (ItemListSerializer, CategoryAddSerializer, ItemAddSerializer)
from rest_framework.views import APIView
from .jobs import ItemJob, CategoryListJob


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
    List Itemspip install -e git+https://github.com/jrief/django-angular#egg=django-angular
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


class HomeView(TemplateView):
    """
    Home view to launch home page
    """
    template_name = "main-content.html"

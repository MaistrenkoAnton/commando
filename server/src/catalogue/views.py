from django.shortcuts import render, HttpResponse
from rest_framework import generics
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer


class CategoryListView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ItemAddView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class CategoryAddView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

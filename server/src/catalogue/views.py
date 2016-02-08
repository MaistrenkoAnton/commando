from rest_framework.response import Response
from rest_framework import generics
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
from rest_framework.views import APIView


class CategoryListView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            cat = Category.objects.filter(parent=None)
        else:
            cat = Category.objects.filter(parent=pk)
        serializer = CategorySerializer(cat, many=True)
        return Response(serializer.data)


class ItemListView(APIView):
    def get(self, request, pk):
        item_list = Item.objects.filter(category=pk).order_by('price')
        serializer = ItemSerializer(item_list, many=True)
        return Response(serializer.data)


class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemAddView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class CategoryAddView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

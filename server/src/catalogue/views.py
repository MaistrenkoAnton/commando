from rest_framework.response import Response
from rest_framework import generics
from .models import Item, Category
from .serializers import ItemListSerializer, CategoryListSerializer, CategoryAddSerializer, ItemDetailSerializer,\
                         ItemAddSerializer
from rest_framework.views import APIView


class CategoryListView(APIView):
    """
    Category List
    pk -- filter by primary key
    """
    serializer = CategoryListSerializer
    model = Category

    def get(self, request, pk=None):
        response_data = self.serializer(self._get_queryset(pk), many=True).data
        return Response(response_data)

    def _get_queryset(self, pk):
        return self.model.objects.filter(parent=pk)


class ItemListView(APIView):
    """
    List Items
    pk -- filter by category
    """
    def get(self, request, pk):
        item_list = Item.objects.filter(category=pk).order_by('price')
        serializer = ItemListSerializer(item_list, many=True)
        return Response(serializer.data)


class ItemDetailView(generics.RetrieveAPIView):
    """
    Get Detail Item by pk
    pk -- particular item's id
    """
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer


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



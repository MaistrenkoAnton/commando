from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import (ItemListSerializer, CategoryAddSerializer, ItemDetailSerializer,
                          ItemAddSerializer, CommentAddSerializer, RateAddSerializer)
from rest_framework.views import APIView
from .models import Item, Category, Comment, Rate
from .jobs import ItemJob, CategoryListJob


class ItemDetailView(APIView):
    """
    Get Detail Item by pk
    pk -- particular item's id
    """
    def get(self, request, pk):
        item = ItemJob().get(pk=str(pk))
        return Response(item)


class CategoryListView(APIView):
    """
    Category List
    pk -- filter by primary key
    """
    def get(self, request, pk=None):
        category_response = CategoryListJob().get(pk=str(pk))
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


class HomeView(TemplateView):
    """
    Home view to launch home page
    """
    template_name = "main-content.html"


class CommentAddView(generics.CreateAPIView):
    """
    Add comment
    """
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentAddSerializer

    def create(self, request, *args, **kwargs):
        """
        Override base method to return value of 'comments_total' field of the related item_object
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "comments_total": Item.objects.get(pk=serializer.data['item']).comments_total
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class SetRateView(generics.CreateAPIView):
    """
    Set rate
    """
    permission_classes = (IsAuthenticated,)
    queryset = Rate.objects.all()
    serializer_class = RateAddSerializer

    def create(self, request, *args, **kwargs):
        """
        Override base method to return value of 'average_rate' field of the related item_object
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "average_rate": Item.objects.get(pk=serializer.data['item']).average_rate
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

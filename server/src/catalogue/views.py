from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Item, Category, Comment
from .serializers import (ItemListSerializer, CategoryListSerializer,
                          CategoryAddSerializer, ItemDetailSerializer,
                          ItemAddSerializer, CommentAddSerializer)
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
    serializer = ItemListSerializer
    model = Item

    def get(self, request, pk):
        response_data = self.serializer(self._get_queryset(pk), many=True).data
        return Response(response_data)

    def _get_queryset(self, pk):
        return self.model.objects.filter(category=pk).order_by('price')


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


class HomeView(TemplateView):
    """
    Home view to launch home page
    """
    template_name = "main-content.html"


from rest_framework_jwt.authentication import  JSONWebTokenAuthentication

class CommentAddView(generics.CreateAPIView):
    """
    Add comment
    """
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentAddSerializer


    def create(self, request, *args, **kwargs):
        data = {
            'text': request.data['text'],
            'item': kwargs['pk'],
            'user': request.user.pk,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # print user
        # new_comment = Comment.objects.create(text=request.data['text'], item=item, user=user)
        # new_comment.save()
        # item.comments_total += 1
        # item.save()
        headers = self.get_success_headers(serializer.data)
        item = Item.objects.get(pk=kwargs['pk'])
        item.comments_total += 1
        item.save()
        response_data = {
            'comments_total': item.comments_total,
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


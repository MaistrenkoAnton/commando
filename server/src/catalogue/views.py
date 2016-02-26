from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import (CategoryAddSerializer, ItemAddSerializer, ItemDetailSerializer,
                          CommentAddSerializer, RateAddSerializer)
from .models import Item, Category, Comment, Rate
from .haystack_serializers import ItemListHaystackSerializer, CategoryListHaystackSerializer
from rest_framework.views import APIView
from .jobs import ItemJob
from haystack.query import SearchQuerySet


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
    serializer = CategoryListHaystackSerializer
    model = Category

    def get(self, request, pk=None):
        response_data = self.serializer(self._get_queryset(pk), many=True).data
        facet = SearchQuerySet().models(self.model).facet('parent').facet_counts()
        return Response({'data': response_data, 'facet': facet})

    def _get_queryset(self, pk):
        return SearchQuerySet().models(self.model).filter(parent=str(pk))


class AllCategoriesListView(APIView):
    """
    All categories list.
    """
    serializer = CategoryListHaystackSerializer
    model = Category

    def get(self, request):
        response_data = self.serializer(self._get_queryset(), many=True).data
        return Response({'data': response_data})

    def _get_queryset(self):
        return SearchQuerySet().models(self.model).all()


class ItemListView(APIView):
    """
    List Items
    pk -- filter by category
    """
    serializer = ItemListHaystackSerializer
    model = Item

    def get(self, request, pk):
        response_data = self.serializer(self._get_queryset(pk), many=True).data
        return Response({'data': response_data})

    def _get_queryset(self, pk):
        return SearchQuerySet().models(self.model).filter(category=pk)


class ItemAddView(generics.CreateAPIView):
    """
    Add Item
    """
    # permission_classes = (IsAdminUser,)
    queryset = Item.objects.all()
    serializer_class = ItemAddSerializer


class ItemUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update Item
    """
    # permission_classes = (IsAdminUser,)
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


class RateAlreadySet(generics.RetrieveAPIView):
    """
    Check if User obj with defined pk already set rate to the Item obj with defined pk
    """
    queryset = Rate.objects.all()
    serializer_class = RateAddSerializer

    def get(self, request, *args, **kwargs):
        response_data = {}
        try:
            Rate.objects.get(user=kwargs['user_pk'], item=kwargs['item_pk'])
            response_data["rate_already_set"] = "true"
        except:
            response_data["rate_already_set"] = "false"
        return Response(response_data)

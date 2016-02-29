from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from catalogue.haystack_serializers import ItemListHaystackSerializer
from catalogue.models import Item
from .models import Store
from .serializers import StoreListSerializer


class StoreListView(generics.ListAPIView):
    """
    Stores List
    """
    serializer_class = StoreListSerializer
    model = Store
    queryset = Store.objects.all()


class StoreDetailView(generics.RetrieveAPIView):
    """
    Store detail
    """
    serializer_class = StoreListSerializer
    model = Store
    queryset = Store.objects.all()


class StoreItemsListView(APIView):
    """
    List Items
    category_pk -- filter by category
    store_pk -- filter by store
    """
    serializer = ItemListHaystackSerializer
    model = Item

    def get(self, request, category_pk, store_pk):
        response_data = self.serializer(self._get_queryset(category_pk, store_pk), many=True).data
        return Response({'data': response_data})

    def _get_queryset(self, category_pk, store_pk):
        return SearchQuerySet().models(self.model).filter(category=category_pk).filter(store=store_pk)

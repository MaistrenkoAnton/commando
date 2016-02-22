from rest_framework import generics
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

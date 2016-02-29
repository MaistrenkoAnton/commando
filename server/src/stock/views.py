
from rest_framework import generics
from .models import Stock
from .serializers import StockListSerializer


class StockListView(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockListSerializer

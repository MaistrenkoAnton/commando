from rest_framework import serializers
from .models import Stock


class StockListSerializer(serializers.ModelSerializer):
    """
    Category List serializer
    """
    class Meta:
        model = Stock
        fields = [ 'store', 'item', 'end_time' , 'new_price']
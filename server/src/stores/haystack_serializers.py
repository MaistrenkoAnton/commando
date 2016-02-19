from drf_haystack.serializers import HaystackSerializer
from .search_indexes import StoreIndex, StoreItemIndex


class StoreListHaystackSerializer(HaystackSerializer):
    """
    Store List serializer
    """
    class Meta:
        index_classes = [StoreIndex]
        fields = ['id', 'title', 'margin', 'activity_status']


class StoreItemListHaystackSerializer(HaystackSerializer):
    """
    List of StoreItems
    Get by category
    """
    class Meta:
        index_classes = [StoreItemIndex]
        fields = [
            'id', 'name', 'price', 'image_url', 'category', 'comments_total', 'average_rate', 'quantity',
            'running_out_level', 'running_out'
        ]

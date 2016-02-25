from drf_haystack.serializers import HaystackSerializer
from .search_indexes import StoreIndex


class StoreListHaystackSerializer(HaystackSerializer):
    """
    Store List serializer
    """
    class Meta:
        index_classes = [StoreIndex]
        fields = ['store_id', 'title', 'margin', 'activity_status']

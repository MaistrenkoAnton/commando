from drf_haystack.serializers import HaystackSerializer
from .search_indexes import ItemIndex, CategoryIndex


class CategoryListHaystackSerializer(HaystackSerializer):
    """
    Category List serializer
    """
    class Meta:
        index_classes = [CategoryIndex]
        fields = ['cat_id', 'name', 'parent']


class ItemListHaystackSerializer(HaystackSerializer):
    """
    List of Items
    Get by category
    """
    class Meta:
        index_classes = [ItemIndex]
        fields = [
            'item_id', 'name', 'price', 'image_url', 'category', 'comments_total', 'average_rate', 'quantity',
            'running_out_level', 'running_out', 'new_price',
        ]

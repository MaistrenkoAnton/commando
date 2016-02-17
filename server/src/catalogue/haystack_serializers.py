from drf_haystack.serializers import HaystackSerializer
from .search_indexes import ItemIndex, CategoryIndex


class CategoryListHaystackSerializer(HaystackSerializer):
    """
    Category List serializer
    """
    class Meta:
        index_classes = [CategoryIndex]
        fields = ['id', 'name', 'parent']


class ItemListHaystackSerializer(HaystackSerializer):
    """
    List of Items
    Get by category
    """
    class Meta:
        index_classes = [ItemIndex]
        fields = [
            "name", "price", "category", "image_url", "description", "id"
        ]

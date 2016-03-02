from drf_haystack.serializers import HaystackSerializer
from .search_indexes import ItemIndex, CategoryIndex


class CategoryListHaystackSerializer(HaystackSerializer):
    """
    Category List serializer
    """
    class Meta:
        index_classes = [CategoryIndex]
        fields = ['cat_id', 'name', 'parent', 'tree_id', 'is_child_node', 'is_leaf_node', 'is_root_node', 'level']


class ItemListHaystackSerializer(HaystackSerializer):
    """
    List of Items
    Get by category
    """
    class Meta:
        index_classes = [ItemIndex]
        fields = ['item_id', 'name', 'price', 'image_url', 'category', 'comments_total', 'average_rate', 'quantity',
                  'store', 'description', 'running_out_level', 'running_out', 'discount']

from rest_framework import serializers
from .models import Category, Item, Comment, Rate
from stores.serializers import StoreListSerializer
from stock.serializers import StockListSerializer


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Category List serializer
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class CategoryAddSerializer(serializers.ModelSerializer):
    """
    Add category
    """
    class Meta:
        model = Category
        fields = ['name', 'parent']


class ItemDetailSerializer(serializers.ModelSerializer):
    """
    Detail Item
    Get by id
    """
    category = CategoryListSerializer()
    stock = StockListSerializer()

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'category', 'description', 'image_url', 'comments_total', 'average_rate',
                  'store', 'quantity', 'running_out_level', 'running_out', 'stock']


class ItemAddSerializer(serializers.ModelSerializer):
    """
    Add Item
    """
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'category', 'description', 'image_url', 'comments_total', 'average_rate',
                  'store', 'quantity', 'running_out_level', 'running_out']
        extra_kwargs = {
            'id': {'read_only': True},
            'average_rate': {'read_only': True},
            'comments_total': {'read_only': True},
            'running_out': {'read_only': True},
        }


class CommentAddSerializer(serializers.ModelSerializer):
    """
    Add comment
    """
    class Meta:
        model = Comment
        fields = ['text', 'item', 'user', 'author']


class RateAddSerializer(serializers.ModelSerializer):
    """
    Add rate
    """
    class Meta:
        model = Rate
        fields = ['rate', 'item', 'user']

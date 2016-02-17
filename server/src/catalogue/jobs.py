from .serializers import ItemDetailSerializer, CategoryListSerializer, CategoryListHaystackSerializer
from .models import Item, Category
from cacheback.base import Job
from haystack.query import SearchQuerySet


class ItemJob(Job):
    """
    Send and get detail info item cache
    """
    def fetch(self, pk):
        return ItemDetailSerializer(Item.objects.get(pk=pk)).data


class CategoryListJob(Job):
    """
    Send and get list categories into cache
    """
    def fetch(self, pk=None):
        #return CategoryListHaystackSerializer(SearchQuerySet().models(Category).filter(parent=pk), many=True).data
        return CategoryListSerializer(Category.objects.filter(parent=pk), many=True).data



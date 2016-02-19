from haystack import indexes
from .models import Store, StoreItem


class StoreItemIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Class for indexing List of StoreItems
    """
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='pk')
    price = indexes.DecimalField(model_attr='price')
    name = indexes.CharField(model_attr='name')
    image_url = indexes.CharField(model_attr='image_url')
    category = indexes.IntegerField(model_attr='category__id')
    description = indexes.CharField(model_attr='description')
    average_rate = indexes.DecimalField(model_attr='average_rate')
    comments_total = indexes.IntegerField(model_attr='comments_total')
    store = indexes.IntegerField(model_attr='store__id')
    quantity = indexes.IntegerField(model_attr='quantity')
    running_out_level = indexes.IntegerField(model_attr='running_out_level')
    running_out = indexes.BooleanField(model_attr='running_out')

    def get_model(self):
        return StoreItem

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()


class StoreIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Class for indexing list of Stores
    """
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='pk')
    title = indexes.CharField(model_attr='title')
    margin = indexes.DecimalField(model_attr='margin')
    activity_status = indexes.BooleanField(model_attr='activity_status')

    def get_model(self):
        return Store

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()

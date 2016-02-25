from haystack import indexes
from .models import Store


class StoreIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Class for indexing list of Stores
    """
    text = indexes.CharField(document=True, use_template=True)
    store_id = indexes.IntegerField(model_attr='pk')
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

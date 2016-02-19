from haystack import indexes
from .models import Item, Category


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Class for indexing List of Items
    """
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='pk')
    price = indexes.CharField(model_attr='price')
    name = indexes.CharField(model_attr='name')
    image_url = indexes.CharField(model_attr='image_url')
    category = indexes.IntegerField(model_attr='category__id')
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Class for indexing list of categories
    """
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='pk')
    name = indexes.CharField(model_attr='name', faceted=True)
    parent = indexes.CharField(model_attr='parent__id', default='None', faceted=True)

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()

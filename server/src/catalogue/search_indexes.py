from haystack import indexes
from .models import Item, Category


class ItemIndex(indexes.SearchIndex, indexes.Indexable):

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
        """Used when the entire index for model is updated."""

        return self.get_model().objects.all().order_by('price')


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='pk')
    name = indexes.CharField(model_attr='name')
    parent = indexes.IntegerField(model_attr='parent__id', default=0)

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

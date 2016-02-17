from haystack import indexes
from .models import Item, Category
from .jobs import ItemJob
from .serializers import ItemDetailSerializer


class ItemIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='pk')
    price = indexes.CharField(model_attr='price')
    name = indexes.CharField(model_attr='name', faceted=True)
    image_url = indexes.CharField(model_attr='image_url')
    category = indexes.IntegerField(model_attr='category__id')
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        for item in self.get_model().objects.all():
            ItemJob().cache_set(str(item.pk), 3600, ItemDetailSerializer(item).data)
        return self.get_model().objects.all()


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='pk')
    name = indexes.CharField(model_attr='name')
    parent = indexes.CharField(model_attr='parent__id', default='None')

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

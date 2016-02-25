from haystack import indexes
from .models import Item, Category


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Class for indexing List of Items
    """
    text = indexes.CharField(document=True, use_template=False)
    item_id = indexes.IntegerField(model_attr='pk')
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
    new_price = indexes.IntegerField(model_attr='stock__new_price', default=0)

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()

    def prepare_image_url(self, obj):
        """
        Prepare image_url field to be displayed correctly
        """
        if obj.image_url:
            return obj.image_url.url
        return


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Class for indexing list of categories
    """
    text = indexes.CharField(document=True, use_template=False)
    cat_id = indexes.IntegerField(model_attr='pk')
    name = indexes.CharField(model_attr='name', faceted=True)
    parent = indexes.CharField(model_attr='parent__id', default='None', faceted=True)

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()

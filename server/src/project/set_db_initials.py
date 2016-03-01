import datetime
from django.utils import timezone
import factory
from catalogue.models import Category, Item
from stores.models import Store
from stock.models import Stock
from cart.models import Cart
import factory.fuzzy


class RandomStoreFactory(factory.django.DjangoModelFactory):
    """
    Generate store object for test purposes
    """
    class Meta:
        model = Store

    title = factory.Faker('company')
    margin = factory.fuzzy.FuzzyDecimal(10.00, 45.00)


class RandomCategoryFactory(factory.django.DjangoModelFactory):
    """
    Generate Category object for test purposes
    """
    class Meta:
        model = Category

    name = factory.fuzzy.FuzzyText(
        prefix=("Cat.  "),
        length=factory.fuzzy.FuzzyInteger(6, 10).fuzz()
    )
    parent = None


class RandomItemFactory(factory.django.DjangoModelFactory):
    """
    Generate Item object for test purposes
    """
    class Meta:
        model = Item

    name = factory.Faker('word')
    price = factory.fuzzy.FuzzyDecimal(100.00, 5000.00)
    description = factory.Faker('text')
    store = factory.Iterator(Store.objects.all())
    category = factory.Iterator(Category.objects.filter(level=2))
    quantity = factory.fuzzy.FuzzyInteger(0, 500)
    running_out_level = factory.fuzzy.FuzzyInteger(10, 50)
    average_rate = factory.fuzzy.FuzzyFloat(0.0, 5.0)


class RandomStockFactory(factory.django.DjangoModelFactory):
    """
    Generate Stock object for test purposes
    """
    class Meta:
        model = Stock

    title = factory.Faker('word')
    store = factory.Iterator(Store.objects.all())
    description = factory.Faker('text')
    discount = factory.fuzzy.FuzzyInteger(5, 90)
    start = factory.fuzzy.FuzzyDateTime(timezone.now()).start_dt
    finish = factory.fuzzy.FuzzyDateTime(timezone.now(),
                                         timezone.now() + datetime.timedelta(120))


class SetUpTestDb(object):
    """
    Generate values for DataBase for test purposes
    """
    @staticmethod
    def clear_all():
        Cart.objects.all().delete()
        Item.objects.all().delete()
        Stock.objects.all().delete()
        Category.objects.all().delete()
        Store.objects.all().delete()
        return True

    @staticmethod
    def set_stores(quantity=5):
        """
        Generate batch of stores
        """
        RandomStoreFactory.create_batch(quantity)
        return True

    @staticmethod
    def set_categories(trees=3):
        """
        Generate batch of categories with 3 levels
        """
        parents = RandomCategoryFactory.create_batch(trees)
        for i in xrange(len(parents)):
            mid_level = RandomCategoryFactory.create_batch(trees, parent=parents[i])
            for j in xrange(len(mid_level)):
                RandomCategoryFactory.create_batch(trees, parent=mid_level[j])
        return True

    @staticmethod
    def set_items():
        """
        Generate batch of items for existing stores and categories
        """
        quantity = Store.objects.count() * Category.objects.filter(level=2).count() * 9
        if quantity == 0:
            return False
        else:
            print "======================================================"
            print "You can make some coffee. And drink it."
            print "It will take several minutes."
            print "======================================================"
            RandomItemFactory.create_batch(quantity)
            return True

    @staticmethod
    def set_stocks():
        """
        Generate batch of stocks for existing stores
        """
        quantity = Store.objects.count() * 3
        if quantity == 0 or Item.objects.count() == 0:
            return False
        else:
            RandomStockFactory.create_batch(quantity)
        return True

    @staticmethod
    def relate_stock_items():
        """
        Generate Stock - Item relations for existing items, stores and stocks
        """
        items = Item.objects.all()
        for item in items:
            if not item.pk % 5:
                stocks = Stock.objects.filter(store_id=item.store_id)
                index_tmp = factory.fuzzy.FuzzyInteger(0, stocks.count() - 1).fuzz()
                item.stock = stocks[index_tmp]
                item.save()
        return True

    @staticmethod
    def set_test_data(stores_qty=5, categories_trees=3):
        """
        Generate full test data for DataBase
        """
        SetUpTestDb.clear_all()
        SetUpTestDb.set_stores(stores_qty)
        SetUpTestDb.set_categories(categories_trees)
        SetUpTestDb.set_items()
        SetUpTestDb.set_stocks()
        SetUpTestDb.relate_stock_items()
        return True

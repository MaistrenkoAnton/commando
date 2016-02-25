from catalogue.models import *
from stores.models import *
import random


def random_word(length):
    """
    Function generates pseudo-rangom string
    """
    import random
    import string
    return ''.join(random.choice(string.lowercase) for i in range(length))


def random_number(x, y):
    """
    Function generates pseudo-random integer
    """
    return random.randint(x, y)


def set_stores(quantity=10):
    for i in xrange(quantity):
        store_title = str(i + 1) + " store"
        margin = random_number(10, 50) + random_number(1, 9)/100
        Store.objects.create(title=store_title, margin=margin)
    return True


def set_categories():
    sub_categories_qty = 3
    top = Category.objects.create(name='top')
    mids = []
    for i in xrange(sub_categories_qty):
        mid_name = "mid " + str(i + 1)
        mids.append(Category.objects.create(name=mid_name, parent=top))
        for j in xrange(sub_categories_qty):
            bot_name = "bot " + str(i + 1)+ '.' + str(j + 1)
            Category.objects.create(name=bot_name, parent=mids[-1])
    return True


def set_items(quantity=10):
    categories = [
        Category.objects.get(name='bot 1.1'),
        Category.objects.get(name='bot 1.2')
    ]
    store = Store.objects.get(title='1 store')

    for i in xrange(2):
        for j in xrange(quantity/2):
            description = ''
            for k in xrange(25):
                description += (' ' + random_word(random_number(2, 15)))
            print description
            Item.objects.create(
                name=("item " + str((j+1) * (i+1))),
                price=(random_number(100, 5000) + random_number(1, 9)/100),
                description=description,
                category=categories[i],
                store=store,
                quantity=random_number(1, 1000),
                running_out_level=random_number(10, 50)
            )
    return True


def set_all_data():
    set_stores()
    set_categories()
    set_items()
    return True
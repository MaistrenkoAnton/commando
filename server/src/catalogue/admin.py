from django.contrib import admin
from .models import Category, Item
from feincms.admin import tree_editor


class CaregoryAdmin(tree_editor.TreeEditor):
    list_display = ('name', )

admin.site.register(Category, CaregoryAdmin)
admin.site.register(Item)

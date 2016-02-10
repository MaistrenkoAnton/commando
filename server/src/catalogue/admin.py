from django.contrib import admin
from .models import Category, Item
from feincms.admin import tree_editor


class CategoryAdmin(tree_editor.TreeEditor):
    list_display = ('name', )
    list_filter = ('name', )


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_url', 'description', 'category')
    list_filter = ('name', )
    ordering = ('price', )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)

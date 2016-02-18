from django.contrib import admin
from .models import Category, Item, Comment, Rate
from feincms.admin import tree_editor


class CategoryAdmin(tree_editor.TreeEditor):
    list_display = ('name', )
    list_filter = ('name', )


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_url', 'description', 'category', 'average_rate', 'comments_total', 'rates_total')
    list_display_links = ('name',)
    list_filter = ('name', )
    ordering = ('price', )
    search_fields = ('name', 'description',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'item', 'author',)
    search_fields = ('item', 'user',)


class RateAdmin(admin.ModelAdmin):
    list_display = ('rate', 'item', 'user',)
    search_fields = ('item', 'user',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rate, RateAdmin)

from django.contrib import admin
from .models import Store, StoreItem


class StoreAdmin(admin.ModelAdmin):
    list_display = ["title", "activity_status"]
    list_display_links = ["title"]
    list_filter = ["title", "activity_status"]
    search_fields = ["title"]

    class Meta:
        model = Store


class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('store', 'name', 'price', 'image_url', 'description', 'category', 'average_rate', 'comments_total', 'rates_total')
    list_display_links = ('name',)
    list_filter = ('name', 'store')
    ordering = ('price', )
    search_fields = ('name', 'description', 'store')

admin.site.register(Store, StoreAdmin)
admin.site.register(StoreItem, StoreItemAdmin)
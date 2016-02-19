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
    list_display = ('name', 'store', 'price', 'quantity', 'running_out_level', 'running_out',
                    'image_url', 'category', 'average_rate', 'comments_total')
    list_display_links = ('name',)
    list_filter = ('category', 'store')
    ordering = ('price', )
    search_fields = ('name', 'description', 'store')

admin.site.register(Store, StoreAdmin)
admin.site.register(StoreItem, StoreItemAdmin)
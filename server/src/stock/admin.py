from django.contrib import admin
from .models import Stock


class StockAdmin(admin.ModelAdmin):
    """
    Customize admin site for Stock model
    """
    list_display = ["title", "store", "discount", "start", "finish"]
    list_display_links = ["title"]
    list_filter = ["store"]
    search_fields = ["title", "description"]

    class Meta:
        model = Stock

admin.site.register(Stock, StockAdmin)

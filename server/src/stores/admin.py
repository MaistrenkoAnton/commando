from django.contrib import admin
from .models import Store


class StoreAdmin(admin.ModelAdmin):
    list_display = ["title", "activity_status"]
    list_display_links = ["title"]
    list_filter = ["title", "activity_status"]
    search_fields = ["title"]

    class Meta:
        model = Store

admin.site.register(Store, StoreAdmin)

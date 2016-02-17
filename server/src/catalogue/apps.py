from django.apps import AppConfig


class CatalogueConfig(AppConfig):
    name = 'catalogue'

    def ready(self):
        from . import signals
        from . import jobs
        from . import serializers

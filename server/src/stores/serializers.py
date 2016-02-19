from rest_framework import serializers
from .models import Store


class StoreListSerializer(serializers.ModelSerializer):
    """
    Store List serializer
    """
    class Meta:
        model = Store
        fields = ['id', 'title', 'margin', 'activity_status']

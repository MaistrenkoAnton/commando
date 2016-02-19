from .serializers import ItemDetailSerializer
from .models import Item
from cacheback.base import Job


class ItemJob(Job):
    """
    Send and get detail info item cache
    """
    def fetch(self, pk):
        return ItemDetailSerializer(Item.objects.get(pk=pk)).data



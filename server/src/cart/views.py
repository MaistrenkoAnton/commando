from rest_framework.response import Response
from rest_framework import views
from rest_framework import status
from .models import Cart
from catalogue.models import Item
from django.contrib.auth.models import User


class CartAddView(views.APIView):
    """
    Create records for purchased items
    """

    def post(self, request):
        """
        Save purchase records for  defined in request items and user
        """
        user = User.objects.get(pk=request.data.get('user'))
        for key in request.data.get('items'):
            item = Item.objects.get(pk=key.get('id'))
            purchase = Cart(user=user, item=item, quantity=key.get('quantity'))
            purchase.save()
        return Response(status=status.HTTP_200_OK)

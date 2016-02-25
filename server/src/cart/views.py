from rest_framework import generics
from .models import Cart
from .serializers import CartAddSerializer


class CartAddView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartAddSerializer


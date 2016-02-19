from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Store
from catalogue.serializers import CommentAddSerializer, RateAddSerializer
from .serializers import StoreListSerializer
from catalogue.models import Category, Comment, Rate
from .haystack_serializers import StoreListHaystackSerializer
from rest_framework.views import APIView
from catalogue.jobs import ItemJob
from haystack.query import SearchQuerySet

# Create your views here.


class StoreListView(generics.ListAPIView):
    """
    Stores List
    """
    serializer_class = StoreListSerializer
    model = Store
    queryset = Store.objects.all()


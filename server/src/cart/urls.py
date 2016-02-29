from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^additemincart/$', views.CartAddView.as_view(), name='add_item_in_cart'),
]

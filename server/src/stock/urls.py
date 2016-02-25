from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^stockdetail/$', views.StockListView.as_view(), name='stock'),
]

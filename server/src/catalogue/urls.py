from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^additem', views.ItemAddView.as_view(), name='add_item'),
    url(r'^categoryadd/$', views.CategoryAddView.as_view(), name='add_category'),
    url(r'^categorylist/(?P<pk>\d+)$', views.CategoryListView.as_view(), name='category_list'),
    url(r'^categorylist/$', views.CategoryListView.as_view(), name='category_list_root'),
    url(r'^itemdetail/(?P<pk>\d+)/$', views.ItemDetailView.as_view(), name='item_detail'),
    url(r'^itemlist/(?P<pk>\d+)/$', views.ItemListView.as_view(), name='item_list'),
    url(r'^$', views.HomeView.as_view(), name='home'),
]

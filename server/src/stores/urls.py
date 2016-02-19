from django.conf.urls import url
from catalogue.views import ItemAddView, ItemUpdateView, ItemUpdateView
from . import views

urlpatterns = [
    url(r'^add-item/$', ItemAddView.as_view(), name='add_item'),
    url(r'^update-delete-item/(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='update_delete_item'),
    # url(r'^delete-item/(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='delete_item'),
    # url(r'^categorylist/$', views.CategoryListView.as_view(), name='category_list_root'),
    # url(r'^itemdetail/(?P<pk>\d+)/$', views.ItemDetailView.as_view(), name='item_detail'),
    # url(r'^itemlist/(?P<pk>\d+)/$', views.ItemListView.as_view(), name='item_list'),
    # url(r'^add-comment/$', views.CommentAddView.as_view(), name='add_comment'),
    # url(r'^set-rate/$', views.SetRateView.as_view(), name='set_rate'),
    url(r'^$', views.StoreListView.as_view(), name='store_list'),
]

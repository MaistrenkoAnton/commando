from django.conf.urls import url
from catalogue.views import ItemAddView, ItemUpdateView
from . import views

urlpatterns = [
    url(r'^add-item/$', ItemAddView.as_view(), name='add_item'),
    url(r'^update-delete-item/(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='update_delete_item'),
    url(r'^account-store/(?P<pk>\d+)/$', views.StoreDetailView.as_view(), name='account_store'),
    url(r'^itemlist/(?P<category_pk>\d+)/(?P<store_pk>\d+)/$', views.StoreItemsListView.as_view(), name='item_list'),
    url(r'^$', views.StoreListView.as_view(), name='store_list'),
]

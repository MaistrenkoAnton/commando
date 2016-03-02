from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^additem/$', views.ItemAddView.as_view(), name='add_item'),
    url(r'^categoryadd/$', views.CategoryAddView.as_view(), name='add_category'),
    url(r'^categories-list/$', views.CategoriesListView.as_view(), name='categories_list'),
    url(r'^itemdetail/(?P<pk>\d+)/$', views.ItemDetailView.as_view(), name='item_detail'),
    url(r'^itemlist/(?P<pk>\d+)/$', views.ItemListView.as_view(), name='item_list'),
    url(r'^add-comment/$', views.CommentAddView.as_view(), name='add_comment'),
    url(r'^set-rate/$', views.SetRateView.as_view(), name='set_rate'),
    url(r'^check-rate-already-set/(?P<user_pk>\d+)/(?P<item_pk>\d+)/$', views.RateAlreadySet.as_view(), name='check_rate_set'),
    url(r'^$', views.HomeView.as_view(), name='home'),
]

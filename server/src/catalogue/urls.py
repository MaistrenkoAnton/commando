from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^additem', views.ItemAddView.as_view()),
    url(r'^categoryadd/$', views.CategoryAddView.as_view()),
    url(r'^categorylist/(?P<pk>\d+)?/?$', views.CategoryListView.as_view()),
]
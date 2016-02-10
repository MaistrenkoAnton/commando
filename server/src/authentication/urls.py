from rest_framework_jwt import views
from django.conf.urls import url
from .views import UserAddView

urlpatterns = [
    url(r'^api-token-auth/', views.obtain_jwt_token),
    url(r'^api-token-refresh/', views.refresh_jwt_token),
    url(r'^api-token-verify/', views.verify_jwt_token),
    url(r'^api-registration/', UserAddView.as_view()),

]

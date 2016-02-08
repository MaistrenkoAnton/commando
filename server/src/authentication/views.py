from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.conf import settings

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r



class UserAddView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        logged_user_data = {}
        if settings.LOGIN_ON_REGISTER:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            user = User.objects.get(pk=serializer.data['id'])
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            logged_user_data = removekey(serializer.data, 'password')
            logged_user_data["token"] = token
        return Response(logged_user_data, status=status.HTTP_201_CREATED, headers=headers)

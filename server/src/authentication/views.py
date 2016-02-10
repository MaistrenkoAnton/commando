from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.response import Response
from .config import *
from .serializers import CreateUserSerializer


class UserAddView(generics.CreateAPIView):
    """
    Class to handle new user registration
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    @staticmethod
    def jwt_response_payload_handler(token, user=None, request=None):
        """
        Override base Django REST JWT utility function to return both token and user object
        """
        return {
            'token': token,
            'user': CreateUserSerializer(user).data
        }

    @staticmethod
    def generate_token(user_id):
        """
        Function generates JWT for defined user object
        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        user = get_object_or_404(User, pk=user_id)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def create(self, request, *args, **kwargs):
        """
        Override base method to return customized data:
            - if "LOGIN_ON_REGISTER = True", return token and user object;
            - if "LOGIN_ON_REGISTER = False", return empty object
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user_data = {}
        if LOGIN_ON_REGISTER:
            token = UserAddView.generate_token(serializer.data["id"])
            user_data = {
                'token': token,
                'user': serializer.data
            }
        return Response(user_data, status=status.HTTP_201_CREATED, headers=headers)

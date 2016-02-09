from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.conf import settings
from .serializers import UserSerializer, jwt_response_payload_handler


def generate_token(user_id):
    """
    Function generates JWT for user object with defined id
    """
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    queryset = User.objects.all()
    user = get_object_or_404(queryset, pk=user_id)
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


class UserAddView(generics.CreateAPIView):
    """
    Class to handle new user registration
    """
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Override basic method to return response user data depending from config  LOGIN_ON_REGISTER setting:
            - if True, return {'id': '<user_id>', 'username': '<username>', 'token': '<generated token>'}
            - if False, return empty dict {}
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(username=serializer.data['username'], password=serializer.data['password'])
        user.save()
        headers = self.get_success_headers(serializer.data)
        logged_user_data = {}
        if settings.LOGIN_ON_REGISTER:
            logged_user_data = jwt_response_payload_handler(generate_token(user.id), user)
        return Response(logged_user_data, status=status.HTTP_201_CREATED, headers=headers)





from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.conf import settings


class UserAddView(generics.CreateAPIView):
    """
    Class to handle new user registration
    """
    serializer_class = UserSerializer

    def generate_token(self, user_id):
        """
        Function generates JWT for user object with defined id
        :param user_id: id of the user object
        :return: generated JWT
        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        user = User.objects.get(pk=user_id)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def remove_key(self, d, key):
        """
        Function returns a clone dictionary with the key item removed
        :param d: base dictionary
        :param key: key of the dictionary item to be removed
        :return: result dictionary with the key item removed
        """
        result_dict = dict(d)
        del result_dict[key]
        return result_dict

    def create(self, request, *args, **kwargs):
        """
        Override basic method to return response user data depending from config  LOGIN_ON_REGISTER setting:
            - if True, return {'id': '<user_id>', 'username': '<username>', 'token': '<generated token>'}
            - if False, return empty dict {}
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logged_user_data = {}
        if settings.LOGIN_ON_REGISTER:
            logged_user_data = self.remove_key(serializer.data, 'password')
            logged_user_data['token'] = self.generate_token(serializer.data['id'])
        return Response(logged_user_data, status=status.HTTP_201_CREATED, headers=headers)







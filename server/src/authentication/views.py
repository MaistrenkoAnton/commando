from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .config import *
from .utils import *
from .serializers import CreateUserSerializer


class UserAddView(generics.CreateAPIView):
    """
    Class to handle new user registration
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        """
        Override base method to return customized data:
            - if "LOGIN_ON_REGISTER = True", return token and user object;
            - if "LOGIN_ON_REGISTER = False", return empty object
        """
        print "here"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user_data = {}
        if LOGIN_ON_REGISTER:
            user = get_object_or_404(User, pk=serializer.data["id"])
            token = generate_token(user)
            user_data = jwt_response_payload_handler(token=token, user=user)
        return Response(user_data, status=status.HTTP_201_CREATED, headers=headers)

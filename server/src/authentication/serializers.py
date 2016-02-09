from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user object
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        write_only_fields = ('password',)


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Override base function to return both token and user object (id and username)
    """
    return {
        'token': token,
        'user': UserSerializer(user).data
    }





from rest_framework_jwt.settings import api_settings
from .serializers import CreateUserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Override base Django REST JWT utility function to return both token and user object
    """
    return {
        'token': token,
        'user': CreateUserSerializer(user).data
    }


def generate_token(user):
        """
        Function generates JWT for defined user object
        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

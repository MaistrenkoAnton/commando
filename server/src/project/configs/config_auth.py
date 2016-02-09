from django.conf import settings
import datetime

# Registration config. Set True for auto log-in when registered
LOGIN_ON_REGISTER = True

# Django REST JWT config
# ----------------------------------------------------------------------------------------------------------------------
JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    # Specify a custom function to generate the token payload
    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    # If you store user_id differently than the default payload handler does, implement this function to fetch
    # user_id from the payload
    # Note: Will be deprecated in favor of JWT_PAYLOAD_GET_USERNAME_HANDLER
    'JWT_PAYLOAD_GET_USER_ID_HANDLER':

    # 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'rest_framework_jwt.utils.jwt_response_payload_handler',
    # Responsible for controlling the response data returned after login or refresh. Override to return a custom
    # response such as including the serialized representation of the User
    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'authentication.serializers.jwt_response_payload_handler',

    # This is the secret key used to sign the JWT.
    'JWT_SECRET_KEY': settings.SECRET_KEY,

    # Algorithm used for generating token
    'JWT_ALGORITHM': 'HS256',

    # f the secret is wrong, it will raise a jwt.DecodeError telling you as such.
    'JWT_VERIFY': True,

    # You can turn off expiration time verification with by setting JWT_VERIFY_EXPIRATION to False.
    'JWT_VERIFY_EXPIRATION': True,

    # This allows you to validate an expiration time which is in the past but no very far.
    'JWT_LEEWAY': 0,

    # This is an instance of Python's datetime.timedelta. This will be added to datetime.
    # utcnow() to set the expiration time
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),

    # his is a string that will be checked against the aud field of the token, if present.
    'JWT_AUDIENCE': None,

    # This is a string that will be checked against the iss field of the token.
    'JWT_ISSUER': None,

    # Enable token refresh functionality. Token issued from rest_framework_jwt.views.obtain_jwt_token
    # will have an orig_iat field
    'JWT_ALLOW_REFRESH': False,

    # Limit on token refresh, is a datetime.timedelta instance. This is how much time after the original token that
    # future tokens can be refreshed from
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
# ----------------------------------------------------------------------------------------------------------------------


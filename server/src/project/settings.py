"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pd(&lbw7(n%z!3b!6@24v$#74*8yy0_1h#9+7g_nn1b=1&^a2u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party apps
    'corsheaders',
    'rest_framework_swagger',
    'rest_framework',
    'mptt',
    'feincms',
    'rest_framework.authtoken',
    'rest_auth',
    # my apps
    'catalogue',
    'authentication',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# Django REST Framework settings
CORS_ORIGIN_ALLOW_ALL = True


MEDIA_ROOT = os.path.join(BASE_DIR, 'files', 'media')
MEDIA_URL = '/media/'



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

    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    # Responsible for controlling the response data returned after login or refresh. Override to return a custom
    # response such as including the serialized representation of the User
    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'authentication.utils.jwt_response_payload_handler',

    # This is the secret key used to sign the JWT.
    'JWT_SECRET_KEY': SECRET_KEY,

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
    'JWT_ALLOW_REFRESH': True,

    # Limit on token refresh, is a datetime.timedelta instance. This is how much time after the original token that
    # future tokens can be refreshed from
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
# ----------------------------------------------------------------------------------------------------------------------

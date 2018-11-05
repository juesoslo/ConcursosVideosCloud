"""
Django settings for project0 project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'eh-%$94j2)r#bo*@o!x#@tf$k_k7*ftah^&ddjz3v##3zq+9+v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'eventos',
    'concursos',
    'plataforma_concurso',
    'proceso_conversion'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project0.urls'

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

WSGI_APPLICATION = 'project0.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

#DATABASE_PASSWORD = os.environ.get("CLOUDG7_DB_PASSWORD", '')
DATABASE_USER = os.environ.get("MONGODB_USER", '')
DATABASE_HOST = os.environ.get("MONGODB_URI", '')
DATABASES = {
    # Connect to my Home Database
    # 'default': {
    #     'NAME': 'cloud',
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'USER': 'postgres',
    #     'PASSWORD': '14827',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # }
    # Connect to my AWS RDS POSTGRES Database
    #'default': {
    #    'NAME': 'cloud',
    #    'ENGINE': 'django.db.backends.postgresql',
    #    'USER': DATABASE_USER,
    #    'PASSWORD': DATABASE_PASSWORD,
    #    'HOST': DATABASE_HOST,
    #    'PORT': '5432',
    #}
    'default': {
        'ENGINE': 'djongo',
        'NAME': DATABASE_USER,
        'HOST': DATABASE_HOST
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'eventos/static'),
    os.path.join(BASE_DIR, 'concursos/static'),
    os.path.join(BASE_DIR, 'plataforma_concurso/static'),
    os.path.join(BASE_DIR, 'proceso_conversion/static'),
    os.path.join(BASE_DIR, 'project0/static'),
)

# Sessions
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

MEDIA_ROOT = os.environ.get("MEDIA_ROOT_FOLDER", os.path.join(BASE_DIR, ''))
MEDIA_URL = '/media/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'organicocooperativa@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get("CLOUDG7_EMAIL_PASS", '')
EMAIL_PORT = 25
EMAIL_USE_TLS = True

#URL final del aplicativo
WEB_URL = os.environ.get("CLOUDG7_WEB_URL", '')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'project0/static'),
#
# ]

# AWS Credentials
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", '')
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID", '')

# AWS storage configuration
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", '')
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = os.environ.get("CLOUDG7_S3_CLOUD_FRONT", '')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

DEFAULT_FILE_STORAGE = 'project0.storage_backends.MediaStorage'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_RELATIVE_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATIC_RELATIVE_LOCATION)

# configuracion de cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            'cloudg7-memcached.jdw0m7.0001.use2.cache.amazonaws.com:11211'
        ]
    }
}

# Descomentar para permitir conexiones de sesion a cache
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Celery
BROKER_URL = "sqs://%s:%s@" % (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_DEFAULT_QUEUE = 'cloudg7-videos-queue'
CELERY_RESULT_BACKEND = None # Disabling the results backend
BROKER_TRANSPORT_OPTIONS = {
    'region': 'us-west-2',
    'polling_interval': 20,
}
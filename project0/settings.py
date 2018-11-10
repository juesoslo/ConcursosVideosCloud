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

# DATABASE_PASSWORD = os.environ.get("CLOUDG7_DB_PASSWORD", '')
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
    # 'default': {
    #    'NAME': 'cloud',
    #    'ENGINE': 'django.db.backends.postgresql',
    #    'USER': DATABASE_USER,
    #    'PASSWORD': DATABASE_PASSWORD,
    #    'HOST': DATABASE_HOST,
    #    'PORT': '5432',
    # }
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

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'eventos/static'),
    os.path.join(BASE_DIR, 'plataforma_concurso/static'),
    os.path.join(BASE_DIR, 'proceso_conversion/static'),
)

# Sessions
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# configuracion de correo
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get("SENDGRID_USERNAME", '')
EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_PASSWORD", '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# URL final del aplicativo
WEB_URL = os.environ.get("CLOUDG7_WEB_URL", '')

# AWS Credentials
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", '')
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", '')
# AWS_S3_REGION_NAME = os.environ.get("AWS_DEFAULT_REGION", '')

# AWS storage configuration
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", '')
AWS_S3_CUSTOM_DOMAIN = os.environ.get("CLOUDG7_S3_CLOUD_FRONT", '')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

MEDIAFILES_LOCATION = 'media'
MEDIA_ROOT = '/%s/' % MEDIAFILES_LOCATION
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'project0.storages.MediaStorage'

STATICFILES_LOCATION = 'static'
STATIC_ROOT = '/%s/' % STATICFILES_LOCATION
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATICFILES_STORAGE = 'project0.storages.StaticStorage'

MEMCACHIER_SERVERS = os.environ.get("MEMCACHIER_SERVERS", '')
MEMCACHIER_USERNAME = os.environ.get("MEMCACHIER_USERNAME", '')
MEMCACHIER_PASSWORD = os.environ.get("MEMCACHIER_PASSWORD", '')

# configuracion de cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        # TIMEOUT is not the connection timeout! It's the default expiration
        # timeout that should be applied to keys! Setting it to `None`
        # disables expiration.
        'TIMEOUT': None,
        'LOCATION': MEMCACHIER_SERVERS,
        'OPTIONS': {
            'binary': True,
            'username': MEMCACHIER_USERNAME,
            'password': MEMCACHIER_PASSWORD,
            'behaviors': {
                # Enable faster IO
                'no_block': True,
                'tcp_nodelay': True,
                # Keep connection alive
                'tcp_keepalive': True,
                # Timeout settings
                'connect_timeout': 2000,  # ms
                'send_timeout': 750 * 1000,  # us
                'receive_timeout': 750 * 1000,  # us
                '_poll_timeout': 2000,  # ms
                # Better failover
                'ketama': True,
                'remove_failed': 1,
                'retry_timeout': 2,
                'dead_timeout': 30,
            }
        }
    }
}

# Descomentar para permitir conexiones de sesion a cache
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Celery
BROKER_URL = "sqs://%s:%s@" % (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
BROKER_TRANSPORT_OPTIONS = {
    'region': 'us-east-1',
    'visibility_timeout': 60,  # 1 minutes
    'polling_interval': 5,  # 5 seconds
}

# CELERY namespaced
CELERY_BROKER_URL = BROKER_URL
CELERY_BROKER_TRANSPORT_OPTIONS = BROKER_TRANSPORT_OPTIONS
CELERY_TASK_DEFAULT_QUEUE = 'cloudg7-videos-queue'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_DEFAULT_QUEUE = 'cloudg7-videos-queue'
CELERY_RESULT_BACKEND = None  # Disabling the results backend

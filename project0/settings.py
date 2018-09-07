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

DATABASES = {
    ## Connect to my Home Database
    # 'default': {
    #     'NAME': 'cloud',
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'OPTIONS' : {
    #             'options': '-c search_path=project0'
    #         },
    #     'USER': 'postgres',
    #     'PASSWORD': '14827',
    #     'HOST': 'localhost',
    #     'PORT': '5434',
    # }
    ## Connect to my AWS Database
    # 'default': {
    #     'NAME': 'baltetlcgm',
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'OPTIONS' : {
    #             'options': '-c search_path=project0'
    #         },
    #     'USER': 'baltetlcgm',
    #     'PASSWORD': 'xkvlx!69',
    #     'HOST': '10.152.166.116',
    #     'PORT': '5432',
    # }
    ## Connect to my Cloud VM Uniandes Database
     # 'default': {
     #     'NAME': 'cloud',
     #     'ENGINE': 'django.db.backends.postgresql',
     #
     #     'OPTIONS' : {
     #             'options': '-c search_path=project0'
     #         },
     #
     #     'OPTIONS': {
     #         'options': '-c search_path=project0'
     #     },
     #
     #     'USER': 'postgres',
     #     'PASSWORD': '14827',
     #     'HOST': '172.24.42.21',
     #     'PORT': '5432',
     # }

    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
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
)

# Sessions
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

MEDIA_ROOT = os.path.join(BASE_DIR, '' )
MEDIA_URL = '/media/'


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'organicocooperativa@gmail.com'
EMAIL_HOST_PASSWORD = 'organico123456'
EMAIL_PORT = 25
EMAIL_USE_TLS = True

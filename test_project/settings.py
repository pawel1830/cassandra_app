"""
Django settings for test_project project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#_7^2-hmz#5#*6qq!_tzu-nv$7v-f@c)jx&8(4=@$!g0h-_-te'

cassandra_hosts = os.environ.get('CASSANDRA_HOSTS', 'localhost')
debug = os.environ.get('DEBUG', 'true').lower() == 'true'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(debug)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django_cassandra_engine',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'test_project.api'
]

MIDDLEWARE = [
]

ROOT_URLCONF = 'test_project.urls'


WSGI_APPLICATION = 'test_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django_cassandra_engine',
        'NAME': 'cassandra_db',
        'TEST_NAME': 'test_db',
        'HOST': cassandra_hosts,
        'OPTIONS': {
            'replication': {
                'strategy_class': 'SimpleStrategy',
                'replication_factor': 1
            }
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'jtestowy21@gmail.com'
EMAIL_HOST_PASSWORD = 'JanTestowyKtoregoMuszeUzyc'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = '1.2.3.4'
# EMAIL_TIMEOUT = 5
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
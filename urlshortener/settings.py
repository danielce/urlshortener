"""
Django settings for urlshortener project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import secret

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_nose',
    'rest_framework',
    'crispy_forms',
    'registration',
    'shortener',
    'control',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'urlshortener.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'control.views.get_configuration',
            ],
        },
    },
]

WSGI_APPLICATION = 'urlshortener.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = secret.DATABASES


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static", "static_root")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", "static_files"),
)


# Django Registration Redux Settings
# One-week activation window; you may, of course, use a different value.
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True  # Automatically log the user in.
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

# Email setttings
EMAIL_HOST = secret.EMAIL_HOST
EMAIL_PORT = secret.EMAIL_PORT
EMAIL_HOST_USER = secret.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secret.EMAIL_HOST_PASSWORD
EMAIL_USE_SSL = secret.EMAIL_USE_SSL

# celery
CELERY_RESULT_BACKEND = "amqp"

# nose
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=shortener',
]

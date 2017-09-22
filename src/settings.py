"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import socket
import django_cache_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '21n1@2(k39!%e$yf4$j14rda--df%*7f_zn04^^w@3xke4l-^%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

HOSTNAME = os.environ.get('HOSTNAME', socket.gethostname())
ALLOWED_HOSTS = [
    '182.16.0.5', 'vagrant', 'webinvoices.eu', 'webinvoices.foggly.net',
    'webinvoices-local.dev']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'debug_toolbar',
    'crispy_forms',
    'django_prices_openexchangerates',
    'rosetta',
    'compressor',
    'django_extensions',
    'import_export',
    'core',
    'invoices',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'invoices.middleware.UserCompanyMiddleware',
    'core.profiling.ProfilerMiddleware',
]

ROOT_URLCONF = 'src.urls'

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
            ]
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
]


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'fakturi'),
        'USER': os.environ.get('DATABASE_USER', 'vagrant'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'vagrant'),
        'TEST': {
            'NAME': 'test_fakturi',
        }
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# Cache
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
CACHES = {}
CACHES['default'] = django_cache_url.config(default=REDIS_URL)
CACHES['default']['TIMEOUT'] = 60
CACHES['default'].setdefault('OPTIONS', {})
CACHES['default']['OPTIONS']['PARSER_CLASS'] = 'redis.connection.HiredisParser'
CACHES['default']['OPTIONS']['MAX_ENTRIES'] = 9999

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'bg'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOGIN_URL = '/login/'

# Email
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

from django.utils.translation import ugettext_lazy as _

LANGUAGES = [
    ('bg', _('Български')),
    ('en', _('Английски')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# Business logic
COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', True)

BASICAUTH = os.environ.get('BASICAUTH', True)
BASICAUTH_USERNAME = os.environ.get('BASICAUTH_USERNAME', 'demo')
BASICAUTH_PASSWORD = os.environ.get('BASICAUTH_PASSWORD', 'demo')

FAKTURI_EIK = os.environ.get("FAKTURI_EIK")
FAKTURI_PASSWORD = os.environ.get("FAKTURI_PASSWORD")
FAKTURI_EXPORT_PATH = os.path.join(BASE_DIR, "crawled", "invoices")

CRISPY_TEMPLATE_PACK = 'semantic-ui'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('semantic-ui')

OPENEXCHANGERATES_API_KEY='3a0c967d227e44bcb6ec3651911fce7d'
OPENEXCHANGERATES_BASE_CURRENCY='USD'

ALLOWED_CURRENCIES = ['BGN', 'USD', 'EUR', 'GBP']

BASE_URL = "http://{}".format(HOSTNAME)
PDF_SERVER = os.environ.get("PDF_SERVER", "http://html2pdf.foggly.net")
CELERY_BROKER_URL = 'redis://localhost:6379/'

GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = 'client_secrets.json'

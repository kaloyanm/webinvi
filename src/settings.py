"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '21n1@2(k39!%e$yf4$j14rda--df%*7f_zn04^^w@3xke4l-^%'

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
    'django.contrib.postgres',
    'debug_toolbar',
    'crispy_forms',
    'rosetta',
    'compressor',
    'django_extensions',
    'import_export',
    'bootstrap3',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
]


CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.environ.get('DATABASE_USER', 'ubuntu'),
        'NAME': os.environ.get('DATABASE_NAME', 'fakturi'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'ubuntu'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', 5432),
        'TEST': {
            'NAME': 'test_fakturi',
        },
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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'bg-BG'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOGIN_URL = '/login/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

from django.utils.translation import ugettext_lazy as _

LANGUAGES = [
    ('es', _('Испански')),
    ('en', _('Английски')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# Business logic
COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', True)

BASIC_AUTH = os.environ.get('BASIC_AUTH', True)
BASICAUTH_USERNAME = os.environ.get('BASICAUTH_USERNAME', 'demo')
BASICAUTH_PASSWORD = os.environ.get('BASICAUTH_PASSWORD', 'demo')

FAKTURI_EIK = os.environ.get("FAKTURI_EIK")
FAKTURI_PASSWORD = os.environ.get("FAKTURI_PASSWORD")
FAKTURI_EXPORT_PATH = os.path.join(BASE_DIR, "crawled", "invoices")

OERATES_APP_ID = os.environ.get("OERATES_APP_ID", "3a0c967d227e44bcb6ec3651911fce7d")
OERATES_BASE_CURRENCY = os.environ.get("OERATES_BASE_CURRENCY", "BGN")

CRISPY_TEMPLATE_PACK = 'semantic-ui'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('semantic-ui')

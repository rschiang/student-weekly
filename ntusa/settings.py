"""
Django settings for NTUSA Student Weekly project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'zh-TW'
TIME_ZONE = 'Asia/Taipei'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
MEDIA_URL = '/media/'
STATIC_URL = '/assets/'
THEME_URL = '/themes/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
THEME_ROOT = os.path.join(BASE_DIR, 'themes')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'vendor/semantic/dist/'),
]

# Core configurations
DEBUG = ('DEBUG' in os.environ)
SECRET_KEY = '<Secret Key>'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dev.sqlite3'),
    }
}

if not DEBUG:
    MEDIA_ROOT = os.environ['DJANGO_MEDIA_ROOT']
    STATIC_ROOT = os.environ['DJANGO_STATIC_ROOT']
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
    ALLOWED_HOSTS = os.environ['SERVER_HOST'].split(',')
    DATABASES['default'] = {
        'ENGINE': ('django.db.backends.mysql'),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', ''),
        'NAME': os.environ.get('DATABASE_NAME', 'weekly'),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
    }

# Application definition
INSTALLED_APPS = [
    'ntusa',
    'issues',
    'templates',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
]

ROOT_URLCONF = 'ntusa.urls'

LOGIN_REDIRECT_URL = 'issues:list'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'ntusa.jinja2.environment',
            'trim_blocks': True,
            'lstrip_blocks': True,
        },
    },
]

SITE_META = {
    'site_name': 'NTU Student Weekly 臺大學生週報',
    'site_short_name': 'NTU Student Weekly',
    'site_vendor': '國立臺灣大學學生會',
    'site_url': 'https://ntustudents.org',
    'site_quote': '我們貢獻這所大學之精神於宇宙。',
}

WSGI_APPLICATION = 'ntusa.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

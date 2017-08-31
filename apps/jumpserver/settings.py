"""
Django settings for jumpserver project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys

from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

sys.path.append(PROJECT_DIR)

# Import project config setting
try:
    from config import config as env_config, env

    CONFIG = env_config.get(env, 'default')()
except ImportError:
    CONFIG = type('_', (), {'__getattr__': lambda arg1, arg2: None})()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.DEBUG or False

# Absolute url for some case, for example email link
SITE_URL = CONFIG.SITE_URL or 'http://localhost'

# LOG LEVEL
LOG_LEVEL = 'DEBUG' if DEBUG else CONFIG.LOG_LEVEL or 'WARNING'

ALLOWED_HOSTS = CONFIG.ALLOWED_HOSTS or []

# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'assets.apps.AssetsConfig',
    'perms.apps.PermsConfig',
    'ops.apps.OpsConfig',
    'audits.apps.AuditsConfig',
    'common.apps.CommonConfig',
    'applications.apps.ApplicationsConfig',
    'rest_framework',
    'rest_framework_swagger',
    'django_filters',
    'bootstrap3',
    'captcha',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'jumpserver.middleware.TimezoneMiddleware',
    'jumpserver.middleware.DemoMiddleware',
]

ROOT_URLCONF = 'jumpserver.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
            ],
        },
    },
]

# WSGI_APPLICATION = 'jumpserver.wsgi.applications'

LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGIN_URL = reverse_lazy('users:login')

SESSION_COOKIE_DOMAIN = CONFIG.SESSION_COOKIE_DOMAIN or None
CSRF_COOKIE_DOMAIN = CONFIG.CSRF_COOKIE_DOMAIN or None
SESSION_COOKIE_AGE = CONFIG.SESSION_COOKIE_AGE or 3600 * 24

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if CONFIG.DB_ENGINE == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': CONFIG.DB_NAME or os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
            'ATOMIC_REQUESTS': False,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.%s' % CONFIG.DB_ENGINE,
            'NAME': CONFIG.DB_NAME,
            'HOST': CONFIG.DB_HOST,
            'PORT': CONFIG.DB_PORT,
            'USER': CONFIG.DB_USER,
            'PASSWORD': CONFIG.DB_PASSWORD,
            'ATOMIC_REQUESTS': False,
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
#
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

# Logging setting
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'main': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(module)s %(levelname)s] %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'main',
            'filename': os.path.join(PROJECT_DIR, 'logs', 'jumpserver.log')
        },
        'ansible_logs': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'main',
            'filename': os.path.join(PROJECT_DIR, 'logs', 'ansible.log')
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': LOG_LEVEL,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'jumpserver': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
        },
        'jumpserver.users.api': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
        },
        'jumpserver.users.view': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
        },
        'ops.ansible_api': {
            'handlers': ['console', 'ansible_logs'],
            'level': LOG_LEVEL,
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# I18N translation
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'), ]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Media files (File, ImageField) will be save these

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/') + '/'

# Use django-bootstrap-form to format template, input max width arg
# BOOTSTRAP_COLUMN_COUNT = 11

# Init data or generate fake data source for development
FIXTURE_DIRS = [os.path.join(BASE_DIR, 'fixtures'), ]

# Email config
EMAIL_HOST = CONFIG.EMAIL_HOST
EMAIL_PORT = CONFIG.EMAIL_PORT
EMAIL_HOST_USER = CONFIG.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = CONFIG.EMAIL_HOST_PASSWORD
EMAIL_USE_SSL = CONFIG.EMAIL_USE_SSL
EMAIL_USE_TLS = CONFIG.EMAIL_USE_TLS
EMAIL_SUBJECT_PREFIX = CONFIG.EMAIL_SUBJECT_PREFIX

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'users.permissions.IsSuperUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.AccessKeyAuthentication',
        'users.authentication.AccessTokenAuthentication',
        'users.authentication.PrivateTokenAuthentication',
        'users.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Custom User Auth model
AUTH_USER_MODEL = 'users.User'

# Auth LDAP settings
if CONFIG.AUTH_LDAP:
    AUTHENTICATION_BACKENDS.insert(0, 'django_auth_ldap.backend.LDAPBackend')
AUTH_LDAP_SERVER_URI = CONFIG.AUTH_LDAP_SERVER_URI
AUTH_LDAP_BIND_DN = CONFIG.AUTH_LDAP_BIND_DN
AUTH_LDAP_BIND_PASSWORD = CONFIG.AUTH_LDAP_BIND_PASSWORD
AUTH_LDAP_USER_DN_TEMPLATE = CONFIG.AUTH_LDAP_USER_DN_TEMPLATE
AUTH_LDAP_START_TLS = CONFIG.AUTH_LDAP_START_TLS
AUTH_LDAP_USER_ATTR_MAP = CONFIG.AUTH_LDAP_USER_ATTR_MAP

# Celery using redis as broker
BROKER_URL = 'redis://:%(password)s@%(host)s:%(port)s/3' % {
    'password': CONFIG.REDIS_PASSWORD if CONFIG.REDIS_PASSWORD else '',
    'host': CONFIG.REDIS_HOST or '127.0.0.1',
    'port': CONFIG.REDIS_PORT or 6379,
}
CELERY_RESULT_BACKEND = BROKER_URL

# TERMINAL_HEATBEAT_INTERVAL = CONFIG.TERMINAL_HEATBEAT_INTERVAL or 30

# crontab job
# CELERYBEAT_SCHEDULE = {
#     Check applications is alive every 10m
# 'check_terminal_alive': {
#     'task': 'applications.tasks.check_terminal_alive',
#     'schedule': timedelta(seconds=TERMINAL_HEATBEAT_INTERVAL),
#     'args': (),
# },
# }


# Cache use redis
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://:%(password)s@%(host)s:%(port)s/4' % {
            'password': CONFIG.REDIS_PASSWORD + '@' if CONFIG.REDIS_PASSWORD else '',
            'host': CONFIG.REDIS_HOST or '127.0.0.1',
            'port': CONFIG.REDIS_PORT or 6379,
        }
    }
}

# Captcha settings, more see https://django-simple-captcha.readthedocs.io/en/latest/advanced.html
CAPTCHA_IMAGE_SIZE = (80, 33)
CAPTCHA_FOREGROUND_COLOR = '#001100'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
CAPTCHA_TEST_MODE = CONFIG.CAPTCHA_TEST_MODE

COMMAND_STORE_BACKEND = 'audits.backends.command.db'
RECORD_STORE_BACKEND = 'audits.backends.record.db'

# Django bootstrap3 setting, more see http://django-bootstrap3.readthedocs.io/en/latest/settings.html
BOOTSTRAP3 = {
    'horizontal_label_class': 'col-md-2',
    # Field class to use in horizontal forms
    'horizontal_field_class': 'col-md-9',
    # Set placeholder attributes to label if no placeholder is provided
    'set_placeholder': True,
}

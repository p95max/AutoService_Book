from pathlib import Path
from decouple import config, Csv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY SETTINGS
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='127.0.0.1', cast=Csv())

# APPLICATIONS
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'crispy_bootstrap5',
    'service_book',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Для статики на Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# URLS & TEMPLATES
ROOT_URLCONF = 'auto_service_book.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'service_book/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'service_book.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'auto_service_book.wsgi.application'

# DATABASE
DATABASES = {}

if DEBUG:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='service_book_db'),
        'USER': config('DB_USER', default='serv_admin'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('LOCAL_DB_HOST', default='localhost'),
        'PORT': config('LOCAL_DB_PORT', default='5433'),
    }
elif config('DOCKER_ENV', default='false').lower() == 'true':
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='service_book_db'),
        'USER': config('DB_USER', default='serv_admin'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DOCKER_DB_HOST', default='db'),
        'PORT': config('DOCKER_DB_PORT', default='5432'),
    }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('RENDER_DB_NAME', default='autoservice_book_db'),
        'USER': config('RENDER_DB_USER', default='autoservice_book_db_user'),
        'PASSWORD': config('RENDER_DB_PASSWORD', default=''),
        'HOST': config('RENDER_DB_HOST', default='dpg-d1leq0re5dus73fkj5d0-a.frankfurt-postgres.render.com'),
        'PORT': config('RENDER_DB_PORT', default='5432'),
    }


# AUTHENTICATION
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'account_login'

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# LOCALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise для статики на Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# Security for Render/prod
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if not host.startswith('127.0.0.1') and not host == 'localhost']

# Admin URL (опционально)
ADMIN_URL = config('ADMIN_URL', default='admin')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

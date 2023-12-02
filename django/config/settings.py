import logging

from os import path
from pathlib import Path

from split_settings.tools import include

from core.config import settings

include(
    'components/database.py',
    'components/templates.py',
    'components/installed_apps.py',
    'components/middleware.py',
    'components/pass_validators.py'
)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=settings.log_level,
                    filename='log/django.log'
                    )

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = settings.securitykey

DEBUG = settings.debug

ALLOWED_HOSTS = settings.allowed_hosts_list

if settings.server_link:
    ALLOWED_HOSTS.append(settings.server_link)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

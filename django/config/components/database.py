from core.config import settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': settings.postgres_db,
        'USER': settings.postgres_user,
        'PASSWORD': settings.postgres_password,
        'HOST': settings.host,
        'PORT': settings.port,
        'OPTIONS': {
            'options': '-c search_path=public,content'
        }
    }
}

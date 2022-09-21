import decouple
import dj_database_url
import django_on_heroku
from .base import *

SECRET_KEY = decouple.config('SECRET_KEY')
ALLOWED_HOSTS = ['.herokuapp.com']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': decouple.config('DB_NAME'),
        'USER': decouple.config('DB_USER'),
        'PASSWORD': decouple.config('DB_PASSWORD'),
        'HOST': decouple.config('DB_HOST'),
        'PORT': decouple.config('DB_PORT', cast=int)
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

django_on_heroku.settings(locals(), staticfiles=False)
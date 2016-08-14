from .base import *
import dj_database_url

ALLOWED_HOSTS = ['*']
DEBUG = False

DATABASES['default'] = dj_database_url.config()
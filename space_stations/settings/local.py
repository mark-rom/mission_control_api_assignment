import os

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5r$znf&moe#q_!4s8qnkm52nwfm@b&qd(fc5vbw=3@!&_x!o0'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

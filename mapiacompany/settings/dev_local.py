from .base   import *

ALLOWED_HOSTS = ['*']

SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')
DEBUG      = True
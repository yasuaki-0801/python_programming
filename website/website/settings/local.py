# settings/local.py
import os
from .base import *
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')  # 環境変数を指定
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')  # 環境変数を指定




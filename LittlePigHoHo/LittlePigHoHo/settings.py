"""
Django settings for LittlePigHoHo project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import yaml
import pymysql
env_dict = os.environ
__conf_yaml_file = env_dict.get('Ho_CONFIG', '/root/LittlePigHoHo/LittlePigHoHo/config.yml')
assert os.path.exists(__conf_yaml_file), 'Not this path'
fp = open(__conf_yaml_file, 'r')
__ho_config = yaml.load(fp.read())
fp.close()
# __ho_config = {}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=0rnw^_t@vny0m-v)i#dnct4s5&8=c9^=s2-uk7q936qswqp=4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# ##################
#      DataBase
# ##################

pymysql.install_as_MySQLdb()

__config_db = __ho_config.get('databases', {})
DATABASES = {
    'default': __config_db.get('server', {})
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# ##################
#      Redis
# ##################
__config_redis = __ho_config.get('redis', {})

# 主redis数据库
REDIS_CONFIG_HOST = __config_redis.get('host', '127.0.0.1')
REDIS_CONFIG_PASSWORD = __config_redis.get('password', '')
REDIS_CONFIG_PORT = __config_redis.get('port', 6379)

# ##################
#      Cache
# ##################

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{0}:{1}'.format(
            __config_redis.get('host', '127.0.0.1'),
            __config_redis.get('port', 6379)
        ),

        'OPTIONS': {
            'DB': 2,
            'PASSWORD': __config_redis.get('password', ''),
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 100,
                'timeout': 10,
            },
        },
    },
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'server.account',
    'server.association',
    'server.school',
    'server.scheduling',
    'server.appraising',
    'server.interview',
    'server.repository',
    'server.task',
    'server.homepage',
    'server.notice'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'common.middlewares.error_handle.HoHoErrorHandleMiddleware',
]


ROOT_URLCONF = 'LittlePigHoHo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "common_static"),
#     'server/homepage/static',  # 用不到的时候可以不写这一行
# )

WSGI_APPLICATION = 'LittlePigHoHo.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = './data/static/'


SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#关闭浏览器进程session失效
# SESSION_COOKIE_AGE = 60 * 60 * 2
# #120分钟之后session失效

# password pbkdf2_sha256$100000$76KK5uuTT38l$J4pdWoq4uNsIjzSoJfC80QbmRtaw9CaKhCzEUJ5nLCE=
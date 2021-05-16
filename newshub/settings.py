"""
Django settings for newshub project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.urls import reverse_lazy


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js', 'serviceworker.js')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9kumj=)%-i6z6lw#e0wgp@sc%y=nyu)#hm14n)gyi=x38$4l#u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['www.moremehub.com', 'moremehub.com']


SITE_ID = 1
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'articles.apps.ArticlesConfig',
    'news_recommendation.apps.NewsRecommendationConfig',
    'account.apps.AccountConfig',
    'actions.apps.ActionsConfig',
    'tagging',
    'sorl.thumbnail',
    'pwa',
    'ckeditor',
    'ckeditor_uploader',
    'django_summernote',
    'storages',


]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'newshub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'newshub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'moreme$moremebas',
        'USER': 'moreme',
        'PASSWORD': '@18061999Ayodeji',
        'HOST': 'moreme.mysql.pythonanywhere-services.com',

    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
"""
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
"""

X_FRAME_OPTIONS = 'ALLOWALL'
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']


##TAGGING CONFIGURATION##
FORCE_LOWERCASE_TAGS = True
MAX_TAG_LENGTH = 20


ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}

LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mail.moremehub@gmail.com'
EMAIL_HOST_PASSWORD = '@18061999Ayo'

PWA_APP_NAME = 'MoremeHub App'
PWA_APP_DESCRIPTION = "Never miss any interesting article on Moremehub Again!"
PWA_APP_THEME_COLOR = '#FFFAFA'
PWA_APP_BACKGROUND_COLOR = '#20B0E9'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {
        'src': '/static/images/moreme_logo160.png',
        'sizes': '160x160',
        'type': 'image/png'
    },{
    'src':'statics/images/moreme_logo192.png',
    'sizes':'192x192',
    'purpose': 'any maskable',
    'type': 'image/png'
    },
{
    'src':'statics/images/moreme_logo512.png',
    'sizes':'512x512',
    'type': 'image/png'
}

]

PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS_APPLE = [
    {
        'src': 'static/images/moreme_logo.jpg',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': 'static/images/moreme_logo630.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

CKEDITOR_UPLOAD_PATH = 'post_images/'
CKEDITOR_CONFIGS = {
    'default':{
        'toolbar': 'Custom',
        'height': '600px',
        'width': '100%',
         'contentsCss': 'img {max-width: 100%;height: auto !important;}',
         'toolbar_Custom': [
            ['Bold', 'Image'],
            ['Link', 'Unlink', 'Anchor'],
            ['Undo', 'Redo', ], ['Styles', 'Format',
                                 'Italic', 'Underline', 'SpellChecker'],
            ['Flash', 'Table', 'HorizontalRule', ],
            ['Smiley', 'SpecialChar'],
            ['BGColor', 'TextColor', 'Source'], ['NumberedList', 'BulletedList',
                                                 'Outdent', 'Indent', 'JustifyCenter', 'JustifyLeft', 'JustifyRight']
                                                 ],
    },
    'special': {
        'toolbar': 'Special',
        'height': '600px',
        'width': '100%',

        'contentsCss': 'img {max-width: 100%;height: auto !important;}',
        'toolbar_Special': [
            ['Bold', 'Youtube', 'Image'],
            ['Wordcount', 'Notification'],
            ['Link', 'Unlink', 'Anchor'],
            ['Undo', 'Redo', ], ['Styles', 'Format',
                                 'Italic', 'Underline', 'SpellChecker'],
            ['Flash', 'Table', 'HorinzontalRule', ],
            ['Smiley', 'SpecialChar'],
            ['BGColor', 'TextColor', 'Source'], ['NumberedList', 'BulletedList',
                                                 'Outdent', 'Indent', 'JustifyCenter', 'JustifyLeft', 'JustifyRight']

        ],
        'extraPlugins': ','.join(['youtube', 'image2', 'wordcount', 'notification']), 'allowedContent': True, 'removePlugins': 'iframe',

    }
}

CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_RESTRICT_BY_USER = True


SUMMERNOTE_CONFIG = {
    'width': '100%',
    'height': '480',
    'toolbar': [
        ['style', ['style']],
        ['font', ['bold', 'italic',]],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']],

        ['insert', ['link', 'picture', 'video',]],
        ['view', ['codeview']],
        ['help', ['help']],
        ],

    'attachment_filesize_limit': 10240 * 10240, # specify the file size
}

AWS_ACCESS_KEY_ID = 'AKIAZI4G35WDQHULEV7Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'darphiz'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'newshub.storage_backends.MediaStorage'

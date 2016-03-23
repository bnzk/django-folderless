"""Settings that need to be set in order to run the tests."""
import os
import sys
import tempfile
import logging
import django.conf.global_settings as DEFAULT_SETTINGS


DEBUG = True

logging.getLogger("factory").setLevel(logging.WARN)

SITE_ID = 1

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."))

# only django 1.7 and up ?!
sys.path.insert(0, APP_ROOT + "/../")

NOSE_ARGS = ['--nocapture',
             '--nologcapture',
             '--exclude-dir=folderless/migrations',
             '--exclude-dir=migrations', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'folderless.tests.urls'

# media root is overridden when needed in tests
MEDIA_ROOT = tempfile.mkdtemp(suffix='folderless_media_root')
MEDIA_URL = "/media/"
FILE_UPLOAD_TEMP_DIR = tempfile.mkdtemp(suffix='folderless_temp')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(APP_ROOT, '../test_app_static')
STATICFILES_DIRS = (
    os.path.join(APP_ROOT, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(APP_ROOT, 'tests/test_app/templates'),
)

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(
    os.path.join(APP_ROOT, 'tests/coverage'))
COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
]

EXTERNAL_APPS = (
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django_nose',
    'easy_thumbnails',
)

INTERNAL_APPS = (
    'folderless',
    'folderless.tests.test_app',
)

MIDDLEWARE_CLASSES = DEFAULT_SETTINGS.MIDDLEWARE_CLASSES + (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS
COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS

SECRET_KEY = 'foobarXXXXY'

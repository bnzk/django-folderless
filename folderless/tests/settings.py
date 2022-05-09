"""Settings that need to be set in order to run the tests."""
import os
import tempfile
import logging
import django

DEBUG = True

logging.getLogger("factory").setLevel(logging.WARN)

SITE_ID = 1

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# only django 1.7 and up ?!
# sys.path.insert(0, APP_ROOT + "/../")

# NOSE_ARGS = ['--nocapture',
#              '--nologcapture',
#              '--exclude-dir=folderless/migrations',
#              '--exclude-dir=migrations', ]

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

if django.VERSION[:2] < (1, 8):
    # List of callables that know how to import templates from various sources.
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )
else:
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
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

# TEMPLATE_DIRS = (
#     os.path.join(APP_ROOT, 'tests/test_app/templates'),
# )

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
    # 'django_nose',
    'easy_thumbnails',
)

INTERNAL_APPS = (
    'folderless',
    'folderless.tests.test_app',
)

MIDDLEWARE = (
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

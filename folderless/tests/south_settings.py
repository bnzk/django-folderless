"""
These settings are used by the ``manage.py`` command.

With normal tests we want to use the fastest possible way which is an
in-memory sqlite database but if you want to create South migrations you
need a persistant database.

Unfortunately there seems to be an issue with either South or syncdb so that
defining two routers ("default" and "south") does not work.

"""
from .test_settings import *  # NOQA


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}

from folderless.utils import DJANGO_1_7_UP
if not DJANGO_1_7_UP:
    print "pre 1.7!"
    INSTALLED_APPS = ('south', ) + INSTALLED_APPS
else:
    print "1.7 up"

MEDIA_ROOT = os.path.join(APP_ROOT, '../test_app_media')
FILE_UPLOAD_TEMP_DIR = None  # django handles this with /tmp, then.

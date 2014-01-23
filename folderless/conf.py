from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import DefaultStorage

from appconf import AppConf


class FolderlessConf(AppConf):
    # could have custom
    FILE_STORAGE = DefaultStorage()
    # could have custom
    THUMBNAIL_STORAGE = DefaultStorage()
    # base upload path
    UPLOAD_TO = 'files'
    # base thumbnails path
    THUMBNAIL_TO = 'thumbs'
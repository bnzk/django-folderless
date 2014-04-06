from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import DefaultStorage

from appconf import AppConf


class FolderlessConf(AppConf):
    DEBUG = False
    # could have custom
    FILE_STORAGE = DefaultStorage()
    # could have custom
    THUMBNAIL_STORAGE = DefaultStorage()
    # base upload path
    UPLOAD_TO = 'files'
    # base thumbnails path
    THUMBNAIL_TO = 'thumbs'
    # convenience
    STATIC_URL = settings.STATIC_URL + "folderless/"
    # Image?
    IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'tif', 'tiff', )
    IMAGE_WIDTH_LIST = '200'
    IMAGE_HEIGHT_LIST = '200'
    IMAGE_WIDTH_FIELD = '100'
    IMAGE_HEIGHT_FIELD = '100'

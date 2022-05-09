from django.conf import settings as django_settings
from django.core.files.storage import DefaultStorage
from django.utils.translation import gettext_lazy as _

from appconf import AppConf


class FolderlessConf(AppConf):

    class Meta:
        proxy = True

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
    STATIC_URL = django_settings.STATIC_URL + "folderless/"
    # Image?
    FILE_TYPES = {
        'image': {
            'title': _(u'Image'),
            'extensions': ('jpg', 'jpeg', 'png', 'gif', 'tif', 'tiff', ),
        },
        'video': {
            'title': _(u'Video'),
            'extensions': ('mp4', 'avi', 'mkv', 'ogg', 'wma', 'mov'),
        },
        'pdf': {
            'title': _(u'PDF document'),
            'extensions': ('pdf'),
        },
        'flash': {
            'title': _(u'Flash'),
            'extensions': ('swf', 'fla', 'as3'),
        },
        'archive': {
            'title': _(u'Archive (zip, etc)'),
            'extensions': ('tgz', 'gzip', 'gz', 'zip', 'tar', 'rar'),
        },
        'audio': {
            'title': _(u'Audio'),
            'extensions': ('mp3', 'wav', 'aac', 'aiff', 'flac'),
        },
        'document': {
            'title': _(u'Text document'),
            'extensions': ('odt', 'doc', 'docx', 'rtf'),
        },
        'spreadsheet': {
            'title': _(u'Spreadsheet'),
            'extensions': ('ods', 'xlsx', 'xls', ),
        },
        'presentation': {
            'title': _(u'Presentation'),
            'extensions': ('ppt', 'pptx', 'odp'),
        },
    }
    IMAGE_WIDTH_LIST = '150'
    IMAGE_HEIGHT_LIST = '150'
    IMAGE_WIDTH_FIELD = '200'
    IMAGE_HEIGHT_FIELD = '150'


settings = FolderlessConf()

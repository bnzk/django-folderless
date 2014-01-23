from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from easy_thumbnails.fields import ThumbnailerField

from conf import FolderlessConf
from conf import settings


class File(models.Model):
    uploader = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        related_name='owned_files',
        null=True, blank=True, verbose_name=_('uploader'))
    created = models.DateTimeField(
        _('created'), editable=False, default=timezone.now)
    modified = models.DateTimeField(
        _('modified'), editable=False, auto_now=True)
    copyright = models.CharField(_('copyright'), max_length=255, blank=True)
    type = models.CharField(
        _('file type'), max_length=12, editable=False, choices=())

    file = ThumbnailerField(_('file'), upload_to=settings.FOLDERLESS_UPLOAD_TO,
                            storage=settings.FOLDERLESS_FILE_STORAGE,
                            thumbnail_storage=settings.FOLDERLESS_THUMBNAIL_STORAGE)
    original_filename = models.CharField(_('original filename'), max_length=255, blank=True, null=True)
    sha1 = models.CharField(_('sha1'), max_length=40, blank=True, default='')
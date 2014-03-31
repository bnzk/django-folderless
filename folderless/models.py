import os
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from easy_thumbnails.fields import ThumbnailerField

from conf import settings


class File(models.Model):
    uploader = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        related_name='owned_files',
        null=True, blank=True, verbose_name=_('uploader'))
    created = models.DateTimeField(
        _('created'), default=timezone.now)
    modified = models.DateTimeField(
        _('modified'), auto_now=True)
    title = models.CharField(_('title'), max_length=255, blank=True)
    author = models.CharField(_('author'), max_length=255, blank=True)
    copyright = models.CharField(_('copyright'), max_length=255, blank=True)
    type = models.CharField(
        _('file type'), max_length=12, choices=(), blank=True)

    file = ThumbnailerField(_('file'), upload_to=settings.FOLDERLESS_UPLOAD_TO,
                            storage=settings.FOLDERLESS_FILE_STORAGE,
                            thumbnail_storage=settings.FOLDERLESS_THUMBNAIL_STORAGE)
    original_filename = models.CharField(_('original filename'), max_length=255, blank=True, null=True)
    sha1 = models.CharField(_('sha1'), max_length=40, blank=True, default='')

    def __unicode__(self):
        return u'%s' % self.original_filename

    def save(self, *args, **kwargs):
        if not self.original_filename:
            self.original_filename = self.file.file
        super(File, self).save(*args, **kwargs)

    @property
    def is_image(self):
        if self.file:
            name, extension = os.path.splitext(self.file.name)
            if extension in settings.FOLDERLESS_IMAGE_TYPES:
                return True
        return False


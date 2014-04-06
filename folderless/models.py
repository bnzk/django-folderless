import os
from django.db import models
from django.core import urlresolvers
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from easy_thumbnails.fields import ThumbnailerField
from easy_thumbnails.files import get_thumbnailer

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
    sha1 = models.CharField(_('Checksum'), help_text=_(u'For preventing duplicates'),max_length=40, blank=True, default='')

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
            if extension[1:] in settings.FOLDERLESS_IMAGE_EXTENSIONS:
                return True
        return False

    @property
    def label(self):
        if self.title:
            return '%s (%s)' % (self.title, self.original_filename)
        else:
            return self.original_filename

    @property
    def admin_url(self):
        return urlresolvers.reverse(
            'admin:%s_%s_change' % (self._meta.app_label,
                                    self._meta.module_name,),
            args=(self.pk,)
        )

    @property
    def thumb_field_url(self):
        if self.is_image:
            return self._thumb_url(settings.FOLDERLESS_IMAGE_WIDTH_FIELD, settings.FOLDERLESS_IMAGE_HEIGHT_FIELD)
        else:
            return

    @property
    def thumb_list_url(self):
        if self.is_image:
            return self._thumb_url(settings.FOLDERLESS_IMAGE_WIDTH_LIST, settings.FOLDERLESS_IMAGE_HEIGHT_LIST)
        else:
            return

    def thumb_list(self):
        if self.is_image:
            url = self._thumb_url(settings.FOLDERLESS_IMAGE_WIDTH_LIST, settings.FOLDERLESS_IMAGE_HEIGHT_LIST)
            return '<a href="%s" target="_blank"><img src="%s" alt="%s"></a>' % (self.file.url, url, self.label)
        else:
            return
    thumb_list.allow_tags = True

    def get_json_response(self):
        return {
            'id': self.id,
            'file_url': self.file.url,
            'edit_url': self.admin_url,
            'thumbnail_list': self.thumb_list_url,
            'thumbnail_field': self.thumb_field_url,
            'label': self.label,
        }

    def _thumb_url(self, width, height):
        thumbnailer = get_thumbnailer(self.file)
        thumbnail_options = {'size': (settings.FOLDERLESS_IMAGE_WIDTH_FIELD, settings.FOLDERLESS_IMAGE_HEIGHT_FIELD)}
        thumb = thumbnailer.get_thumbnail(thumbnail_options)
        return thumb.url

    @property
    def url(self):
        """
        to make the model behave like a file field
        """
        try:
            r = self.file.url
        except:
            r = ''
        return r

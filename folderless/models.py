import os
from django.db import models
from django.core import urlresolvers
from django.conf import settings
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from easy_thumbnails.fields import ThumbnailerField
from easy_thumbnails.files import get_thumbnailer

from conf import settings

OTHER_TYPE = 'other'

class File(models.Model):
    uploader = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        related_name='owned_files',
        null=True, blank=True, verbose_name=_('Uploader'))
    created = models.DateTimeField(
        _('Created'), default=timezone.now)
    modified = models.DateTimeField(
        _('Modified'), auto_now=True)
    title = models.CharField(_('Title'), max_length=255, blank=True)
    author = models.CharField(_('Author'), max_length=255, blank=True)
    copyright = models.CharField(_('Copyright'), max_length=255, blank=True)
    type = models.CharField(
        _('File type'), max_length=12, choices=(), blank=True)

    file = ThumbnailerField(_('File'), upload_to=settings.FOLDERLESS_UPLOAD_TO,
                            storage=settings.FOLDERLESS_FILE_STORAGE,
                            thumbnail_storage=settings.FOLDERLESS_THUMBNAIL_STORAGE)
    original_filename = models.CharField(_('Original filename'), max_length=255, blank=True, null=True)
    extension = models.CharField(_('Extension'), max_length=255, blank=True, null=True)
    sha1 = models.CharField(_('Checksum'), help_text=_(u'For preventing duplicates'),max_length=40, blank=True, default='')

    def __unicode__(self):
        return u'%s' % self.original_filename

    class Meta:
        verbose_name = _(u'File')
        verbose_name_plural = _(u'Files')

    def save(self, *args, **kwargs):
        if not self.original_filename:
            self.original_filename = self.file.file
        super(File, self).save(*args, **kwargs)

    @property
    def is_image(self):
        if self.file:
            image_definition = settings.FOLDERLESS_FILE_TYPES.get('image', None)
            if not image_definition is None:
                if self.extension in image_definition.get('extensions'):
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
            url = self.thumb_list_url
            return '<a href="%s" target="_blank"><img src="%s" alt="%s"></a>' % (self.file.url, url, self.label)
        else:
            return
    thumb_list.allow_tags = True
    thumb_list.short_description = _(u'Thumb')

    def references_list(self):
        links = [rel.get_accessor_name() for rel in File._meta.get_all_related_objects()]
        total = 0
        for link in links:
            total += getattr(self, link).all().count()
            #objects = getattr(File, link).all()
            #for object in objects:
                # do something with related object instance
        if total > 0:
            return "%sx" % total
        else:
            return "-"
    references_list.allow_tags = True
    references_list.short_description = _(u'Referenced?')

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

@receiver(pre_save, sender=File, dispatch_uid="folderless_file_processing")
def folderless_file_processing(sender, **kwargs):
    instance = kwargs.get("instance")
    if instance.file:
        name, extension = os.path.splitext(instance.file.name)
        if len(extension) > 1:
            instance.extension = extension[1:].lower()
        else:
            instance.extension = ''
        instance.type = OTHER_TYPE
        for type, definition in settings.FOLDERLESS_FILE_TYPES.iteritems():
            if instance.extension in definition.get("extensions"):
                instance.type = type

# do this with a signal, to catch them all
@receiver(pre_delete, sender=File)
def cleanup_file_on_delete(sender, instance, **kwargs):
    print instance.file.__dict__
    instance.file.delete(False)
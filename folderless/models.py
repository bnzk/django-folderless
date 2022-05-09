import os
from django.core.exceptions import ValidationError
from django.core.files.base import File as DjangoFile
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from easy_thumbnails.fields import ThumbnailerField
from easy_thumbnails.files import get_thumbnailer

from .conf import settings
from folderless.utils import get_valid_filename, sha1_from_file, model_get_all_related_objects

# compat
import django
if django.VERSION[:2] < (1, 10):
    from django.core import urlresolvers
else:
    from django import urls as urlresolvers


OTHER_TYPE = 'other'


class File(models.Model):
    file = ThumbnailerField(
        _('File'), upload_to=settings.FOLDERLESS_UPLOAD_TO,
        storage=settings.FOLDERLESS_FILE_STORAGE,
        thumbnail_storage=settings.FOLDERLESS_THUMBNAIL_STORAGE)
    name = models.CharField(
        _('name'), max_length=255, blank=True, default='')
    filename = models.CharField(
        _('Filename'),
        help_text=_(u'Use for renaming your file on the server'),
        max_length=255, blank=False, unique=True)
    author = models.CharField(
        _('Author'), max_length=255, blank=True, default='')
    copyright = models.CharField(
        _('Copyright'), max_length=255, blank=True, default='')
    type = models.CharField(
        _('File type'), max_length=12, choices=(), blank=True)
    uploader = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='owned_files',
        verbose_name=_('Uploader'),
    )
    created = models.DateTimeField(
        _('Created'), default=timezone.now)
    modified = models.DateTimeField(
        _('Modified'), auto_now=True)
    extension = models.CharField(
        _('Extension'), max_length=255, blank=True, default='')
    file_hash = models.CharField(
        _('Checksum'), help_text=_(u'For preventing duplicates'),
        max_length=40, blank=False, unique=True)

    def __str__(self):
        return '%s' % self.filename

    class Meta:
        verbose_name = _(u'File')
        verbose_name_plural = _(u'Files')

    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = self.file.file
        super(File, self).save(*args, **kwargs)

    # you should not change extensions!
    def clean(self, *args, **kwargs):
        super(File, self).clean(*args, **kwargs)
        if (self.id):
            old_instance = File.objects.get(pk=self.id)
            if not old_instance.filename == self.filename:
                self.filename = get_valid_filename(self.filename)
                old_name, old_extension = os.path.splitext(old_instance.filename)
                new_name, new_extension = os.path.splitext(self.filename)
                if not old_extension.lower() == new_extension.lower():
                    raise ValidationError(_("File extension must stay the same."))

    def generate_file_hash(self):
        self.file_hash = sha1_from_file(self.file)

    @property
    def is_image(self):
        if self.file:
            image_definition = settings.FOLDERLESS_FILE_TYPES.get(
                'image', None)
            if image_definition is not None:
                if self.extension in image_definition.get('extensions'):
                    return True
        return False

    @property
    def label(self):
        if self.name:
            return '%s (%s)' % (self.name, self.filename)
        else:
            return self.filename

    @property
    def admin_url(self):
        return urlresolvers.reverse(
            'admin:folderless_file_change',
            args=(self.pk,)
        )

    @property
    def thumb_field_url(self):
        if self.is_image:
            return self._thumb_url(
                settings.FOLDERLESS_IMAGE_WIDTH_FIELD,
                settings.FOLDERLESS_IMAGE_HEIGHT_FIELD)
        else:
            return

    @property
    def thumb_list_url(self):
        if self.is_image:
            return self._thumb_url(
                settings.FOLDERLESS_IMAGE_WIDTH_LIST,
                settings.FOLDERLESS_IMAGE_HEIGHT_LIST)
        else:
            return

    def thumb_list(self):
        if self.is_image:
            url = self.thumb_list_url
            return mark_safe('<a href="%s" target="_blank"><img src="%s" alt="%s"></a>'
                   % (self.file.url, url, self.label))
        else:
            return

    thumb_list.allow_tags = True
    thumb_list.short_description = _(u'Thumb')

    def references_list(self):
        links = [
            rel.get_accessor_name()
            for rel in model_get_all_related_objects(File)
        ]
        total = 0
        for link in links:
            total += getattr(self, link).all().count()
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
        if self.file:

            thumbnailer = get_thumbnailer(self.file)
            thumbnail_options = {
                'size': (width, height)
            }
            try:
                # catch the value error when trying to resize a 600x1 pixel image
                # to 150x150 > PIL wants to do it 150x0, and then complains...
                thumb = thumbnailer.get_thumbnail(thumbnail_options)
                return thumb.url
            except ValueError:
                pass
        return ''

    @property
    def url(self):
        """
        to make the model behave like a file field
        """
        if self.file:
            return self.file.url
        return ''


@receiver(pre_save, sender=File, dispatch_uid="folderless_file_processing")
def folderless_file_processing(sender, **kwargs):
    """
    what we do here:
    - determine file type, set it.
    - generate file hash
    - check for file renames
    """
    instance = kwargs.get("instance")
    if instance.file:
        name, extension = os.path.splitext(instance.file.name)
        if len(extension) > 1:
            instance.extension = extension[1:].lower()
        else:
            instance.extension = ''
        instance.type = OTHER_TYPE
        for type, definition in settings.FOLDERLESS_FILE_TYPES.items():
            if instance.extension in definition.get("extensions"):
                instance.type = type
        instance.generate_file_hash()
        if instance.id:
            old_instance = File.objects.get(pk=instance.id)
            if not old_instance.filename == instance.filename:
                # rename!
                new_file = DjangoFile(open(instance.file.path, mode='rb'))
                instance.file.delete(False)  # remove including thumbs
                instance.file.save(instance.filename, new_file, save=False)


# do this with a signal, to catch them all
@receiver(pre_delete, sender=File)
def cleanup_file_on_delete(sender, instance, **kwargs):
    # includes thumbnails
    instance.file.delete(False)

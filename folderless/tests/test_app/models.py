from django.db import models
from django.conf import settings

from folderless.fields import FolderlessFileField


class TestModel(models.Model):
    dummy = models.CharField('dummy', max_length=255, blank=True)
    file = FolderlessFileField(blank=True, null=True)
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
                             help_text=u'only for checking out raw_id_fields!',
                             blank=True, null=True, default=None,
                             on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.dummy


class TestGallery(models.Model):
    title = models.CharField('Title', null=True, blank=True, default='', max_length=255)

    def __unicode__(self):
        return self.title


class TestGalleryEntry(models.Model):
    # file = FilerFileField(null=True, blank=True, default=None, verbose_name=_("File"))
    image = FolderlessFileField(null=True, blank=True, default=None, verbose_name=("File"))
    description = models.CharField('description', null=True, blank=True, default='', max_length=255)
    gallery = models.ForeignKey(
        TestGallery,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = u"Test Gallery ENTRY"

    def __unicode__(self):
        return str(self.image)

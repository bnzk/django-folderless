from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from folderless.fields import FolderlessFileField


class TestModel(models.Model):
    dummy = models.CharField(_('dummy'), max_length=255, blank=True)
    file = FolderlessFileField(blank=True, null=True)
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
                             help_text=u'only for checking out raw_id_fields!', blank=True, null=True, default=None)
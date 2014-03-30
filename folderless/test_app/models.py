from django.db import models
from django.utils.translation import ugettext_lazy as _

from folderless.fields import FolderlessFileField


class TestModel(models.Model):
    dummy = models.CharField(_('dummy'), max_length=255, blank=True)
    file = FolderlessFileField(blank=True, null=True)
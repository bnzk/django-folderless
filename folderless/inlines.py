# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
# from django.conf import settings as globalsettings
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.contrib.admin.sites import site
# from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from folderless.models import File
from django.conf import settings


# this part is mostly inspired by django-filer: https://github.com/stefanfoulis/django-filer/blob/develop/filer/fields/file.py
# uploader basics: https://github.com/blueimp/jQuery-File-Upload/wiki/Basic-plugin
class FolderlessFileInlineMixin():

    class Media:
        js = (
            settings.FOLDERLESS_STATIC_URL + 'js/jquery.folderless_add_inline.js',
        )

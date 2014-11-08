#-*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.util import unquote
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from folderless.models import File


class FileAdminChangeFrom(forms.ModelForm):
    class Meta:
        model = File
        # exclude = ("file_hash", "original_filename")
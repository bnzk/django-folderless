# -*- coding: utf-8 -*-
import os
from distutils.version import LooseVersion

import django
from django.utils.text import get_valid_filename as get_valid_filename_django
from django.template.defaultfilters import slugify
# from django.core.files.uploadedfile import SimpleUploadedFile


DJANGO_1_7_UP = LooseVersion(django.get_version()) >= LooseVersion('1.7')


class UploadException(Exception):
    pass


# thank you, django-filer!

def handle_upload(request):
    if not request.method == "POST":
        raise UploadException("AJAX request not valid: must be POST")
    if len(request.FILES) == 1:
        # print "not raw!"
        # FILES is a dictionary in Django but Ajax Upload gives the uploaded file an
        # ID based on a random number, so it cannot be guessed here in the code.
        # Rather than editing Ajax Upload to pass the ID in the querystring, note that
        # each upload is a separate request so FILES should only have one entry.
        # Thus, we can just grab the first (and only) value in the dict.
        is_raw = False
        upload = list(request.FILES.values())[0]
        filename = upload.name
    else:
        raise UploadException("AJAX request not valid: Bad Upload")
    return upload, filename, is_raw


def get_valid_filename(s):
    """
    like the regular get_valid_filename, but also slugifies away
    umlauts and stuff.
    """
    s = get_valid_filename_django(s)
    filename, ext = os.path.splitext(s)
    filename = slugify(filename)
    ext = slugify(ext)
    if ext:
        return "%s.%s" % (filename, ext)
    else:
        return "%s" % (filename,)

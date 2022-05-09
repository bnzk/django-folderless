import hashlib
import os
from distutils.version import LooseVersion

import django
from django.utils.text import get_valid_filename as get_valid_filename_django
from django.template.defaultfilters import slugify
# from django.core.files.uploadedfile import SimpleUploadedFile


DJANGO_1_7_UP = LooseVersion(django.get_version()) >= LooseVersion('1.7')


class UploadException(Exception):
    pass


def model_get_all_related_objects(model):
    """
    https://docs.djangoproject.com/en/2.0/ref/models/meta/
    """
    if getattr(model._meta, 'get_all_related_objects', None):
        return model._meta.get_all_related_objects()
    else:
        return [
            f for f in model._meta.get_fields()
            if (f.one_to_many or f.one_to_one)
            and f.auto_created
            and not f.concrete
        ]


def sha1_from_file(file):
    sha = hashlib.sha1()
    file.seek(0)
    while True:
        # digest size for sha1 is 160 bytes, so a multiple should do best.
        buf = file.read(160000)
        if not buf:
            break
        sha.update(buf)
    file_hash = sha.hexdigest()
    # to make sure later operations can read the whole file
    file.seek(0)
    return file_hash


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
        if request.POST.get("filename", None):
            filename = request.POST.get("filename")
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

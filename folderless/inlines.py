# -*- coding: utf-8 -*-

from django.conf import settings


# for the future
class FolderlessMultiUploadInlineMixin():

    class Media:
        js = (
            settings.FOLDERLESS_STATIC_URL + 'js/jquery.folderless_multiupload.js',
        )

# -*- coding: utf-8 -*-
import os
from django.test import TestCase
from django.core.files import File as DjangoFile
from django.conf import settings

from folderless.models import File
from folderless.tests.utils import create_superuser, create_image


class FolderlessModelsTests(TestCase):

    def setUp(self):
        self.superuser = create_superuser()
        self.client.login(username='admin', password='secret')
        self.img = create_image()
        self.image_name = 'test_file.jpg'
        self.filename = os.path.join(settings.FILE_UPLOAD_TEMP_DIR,
                                     self.image_name)
        self.img.save(self.filename, 'JPEG')

    def tearDown(self):
        self.client.logout()
        os.remove(self.filename)
        for f in File.objects.all():
            f.delete()

    def _create_file(self):
        file_obj = DjangoFile(open(self.filename), name=self.image_name)
        image = File.objects.create(uploader=self.superuser,
                                    original_filename=self.image_name,
                                    file=file_obj)
        return image

    def test_create_and_delete_file(self):
        self.assertEqual(File.objects.count(), 0)
        file = self._create_file()
        file.save()
        self.assertEqual(File.objects.count(), 1)
        file = File.objects.all()[0]
        self.assertEqual(True, os.path.isfile(file.file.path))
        file.delete()
        self.assertEqual(File.objects.count(), 0)

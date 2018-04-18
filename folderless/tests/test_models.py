# -*- coding: utf-8 -*-
import hashlib
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
        file_obj = DjangoFile(open(self.filename, 'rb'), name=self.image_name)
        image = File.objects.create(uploader=self.superuser,
                                    filename=self.image_name,
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

    def test_file_hash_set(self):
        file = self._create_file()
        file.save()
        os_file = open(self.filename, "rb")
        sha = hashlib.sha1()
        os_file.seek(0)
        while True:
            # digest size for sha1 is 160 bytes, so a multiple should do best.
            buf = os_file.read(160)
            if not buf:
                break
            sha.update(buf)
        file_hash = sha.hexdigest()
        self.assertEqual(file.file_hash, file_hash)

    def test_rename_file(self):
        self.assertEqual(File.objects.count(), 0)
        file = self._create_file()
        old_path = file.file.path
        file.filename = '1234.jpg'
        file.save()
        self.assertNotEqual(old_path, file.file.path,
                            "File has still the same filename/path (%s)" % old_path)
        self.assertTrue('1234.jpg' in file.file.path, "File was not renamed to 1234.jpg")
        self.assertEqual(True, os.path.isfile(file.file.path), "File does not exist as renamed.")
        self.assertEqual(False, os.path.isfile(old_path),
                         "File was renamed, but original is still there!")
        file.delete()
        self.assertEqual(File.objects.count(), 0)

# -*- coding: utf-8 -*-

# from django.forms.models import modelform_factory
import os
import json

from django.test import TestCase
# from django.core.files import File as DjangoFile
from django.core.urlresolvers import reverse

from django.conf import settings

from folderless.models import File
from folderless.tests.utils import create_superuser, create_image


class FolderlessAdminUrlsTests(TestCase):
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

    def test_app_index_get(self):
        response = self.client.get(reverse('admin:app_list', args=('folderless',)))
        self.assertEqual(response.status_code, 200)

    def test_file_list(self):
        response = self.client.get(reverse('admin:folderless_file_changelist'))
        self.assertEqual(response.status_code, 200)

    # TODO: write field test with test app.
    def test_file_field_empty(self):
        pass
        # response = self.client.get(reverse('admin:test_app_file_changelist'))
        # self.assertEqual(response.status_code, 200)

    def test_file_upload(self):
        self.assertEqual(File.objects.count(), 0)
        self.client.post(
            reverse('admin:folderless-ajax_upload'),
            {'ajax-file': open(self.filename), 'filename': self.image_name}
        )
        self.assertEqual(File.objects.count(), 1)

    def test_non_post_upload_request(self):
        self.assertEqual(File.objects.count(), 0)
        response = self.client.get(reverse('admin:folderless-ajax_upload'))
        data = json.loads(response.content)
        self.assertEqual(data["success"], False)

    def test_prevent_duplicate_file_name_upload(self):
        self.assertEqual(File.objects.count(), 0)
        self.client.post(
            reverse('admin:folderless-ajax_upload'),
            {'ajax-file': open(self.filename), 'filename': self.image_name}
        )
        self.assertEqual(File.objects.count(), 1)
        self.client.post(
            reverse('admin:folderless-ajax_upload'),
            {'ajax-file': open(self.filename), 'filename': self.image_name}
        )
        self.assertEqual(File.objects.count(), 1)

    def test_prevent_duplicate_file_content_upload(self):
        self.assertEqual(File.objects.count(), 0)
        self.client.post(
            reverse('admin:folderless-ajax_upload'),
            {'ajax-file': open(self.filename), 'filename': "first-%s" % self.image_name}
        )
        self.assertEqual(File.objects.count(), 1)
        self.client.post(
            reverse('admin:folderless-ajax_upload'),
            {'ajax-file': open(self.filename), 'filename': "second-%s" % self.image_name}
        )
        self.assertEqual(File.objects.count(), 1)

    def test_prevent_duplicate_json_response(self):
        self.assertEqual(File.objects.count(), 0)
        self.client.post(
            reverse('admin:folderless-ajax_upload'),
            {'ajax-file': open(self.filename), 'filename': "first-%s" % self.image_name}
        )
        self.assertEqual(File.objects.count(), 1)
        response = self.client.post(
            reverse('admin:folderless-ajax_upload'),
            {'ajax-file': open(self.filename), 'filename': "second-%s" % self.image_name}
        )
        data = json.loads(response.content)
        self.assertEqual(data["success"], False)
        self.assertGreaterEqual(data["errors"], 1)

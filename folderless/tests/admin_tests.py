# -*- coding: utf-8 -*-

# from django.forms.models import modelform_factory
from django.test import TestCase
# from django.core.files import File as DjangoFile
from django.core.urlresolvers import reverse
# from django.conf import settings

# from folderless.models import File
from folderless.tests.utils import create_superuser  # , create_image


class FolderlessAdminUrlsTests(TestCase):
    def setUp(self):
        self.superuser = create_superuser()
        self.client.login(username='admin', password='secret')

    def tearDown(self):
        self.client.logout()

    def test_app_index_get(self):
        response = self.client.get(reverse('admin:app_list', args=('folderless',)))
        self.assertEqual(response.status_code, 200)

    def test_file_list(self):
        response = self.client.get(reverse('admin:folderless_file_changelist'))
        self.assertEqual(response.status_code, 200)

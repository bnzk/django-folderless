# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import folderless.fields


class Migration(migrations.Migration):

    dependencies = [
        ('folderless', '0001_initial'),
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=255, null=True, verbose_name=b'Title', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestGalleryEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=b'', max_length=255, null=True, verbose_name=b'description', blank=True)),
                ('gallery', models.ForeignKey(on_delete=models.CASCADE, to='test_app.TestGallery')),
                ('image', folderless.fields.FolderlessFileField(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='folderless.File', null=True, verbose_name=b'File')),
            ],
            options={
                'verbose_name': 'Test Gallery ENTRY',
            },
            bases=(models.Model,),
        ),
    ]

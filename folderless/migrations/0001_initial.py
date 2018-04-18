# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.files.storage
from django.conf import settings
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', easy_thumbnails.fields.ThumbnailerField(upload_to=b'files', storage=django.core.files.storage.FileSystemStorage(), verbose_name='File')),
                ('name', models.CharField(default=b'', max_length=255, verbose_name='name', blank=True)),
                ('filename', models.CharField(help_text='Use for renaming your file on the server', unique=True, max_length=255, verbose_name='Filename')),
                ('author', models.CharField(default=b'', max_length=255, verbose_name='Author', blank=True)),
                ('copyright', models.CharField(default=b'', max_length=255, verbose_name='Copyright', blank=True)),
                ('type', models.CharField(max_length=12, verbose_name='File type', blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('extension', models.CharField(default=b'', max_length=255, verbose_name='Extension', blank=True)),
                ('file_hash', models.CharField(help_text='For preventing duplicates', unique=True, max_length=40, verbose_name='Checksum')),
                ('uploader', models.ForeignKey(related_name='owned_files', verbose_name='Uploader', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
            bases=(models.Model,),
        ),
    ]

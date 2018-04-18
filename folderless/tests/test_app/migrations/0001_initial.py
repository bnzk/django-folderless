# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import folderless.fields


class Migration(migrations.Migration):

    dependencies = [
        ('folderless', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dummy', models.CharField(max_length=255, verbose_name=b'dummy', blank=True)),
                ('file', folderless.fields.FolderlessFileField(on_delete=django.db.models.deletion.PROTECT, blank=True, to='folderless.File', null=True)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, default=None, blank=True, to=settings.AUTH_USER_MODEL, help_text='only for checking out raw_id_fields!', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

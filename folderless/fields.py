#-*- coding: utf-8 -*-
import inspect
from django import forms
from django.conf import settings as globalsettings
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.contrib.admin.sites import site
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from folderless.models import File
from django.conf import settings


# this part is mostly inspired by django-filer: https://github.com/stefanfoulis/django-filer/blob/develop/filer/fields/file.py
# uploader basics: https://github.com/blueimp/jQuery-File-Upload/wiki/Basic-plugin
class FolderlessFileWidget(ForeignKeyRawIdWidget):
    choices = None

    def render(self, name, value, attrs=None):
        obj = self.obj_for_value(value)
        #related_url = reverse('admin:filer-directory_listing-last')
        related_url = reverse('admin:folderless_file_changelist')

        if value:
            try:
                file_obj = File.objects.get(pk=value)
            except Exception as e:
                if settings.FOLDERLESS_DEBUG:
                    raise
        params = self.url_parameters()
        if params:
            lookup_url = '?' + '&amp;'.join(
                                ['%s=%s' % (k, v) for k, v in list(params.items())])
        else:
            lookup_url = ''
        if not 'class' in attrs:
            # The JavaScript looks for this hook.
            attrs['class'] = 'vForeignKeyRawIdAdminField'
        else:
            attrs['class'] += ' vForeignKeyRawIdAdminField'
        # rendering the super for ForeignKeyRawIdWidget on purpose here because
        # we only need the input and none of the other stuff that
        # ForeignKeyRawIdWidget adds
        hidden_input = super(ForeignKeyRawIdWidget, self).render(
                                                            name, value, attrs)
        css_id = attrs.get('id', 'id_file_x')
        context = {
            'folderless_static': settings.STATIC_URL + "folderless",
            'hidden_input': hidden_input,
            'lookup_url': '%s%s' % (related_url, lookup_url),
            'object': obj,
            'size': settings.FOLDERLESS_IMAGE_SIZE_FIELD,
            'lookup_id': 'lookup_%s',
            'clear_id': '%s_clear' % css_id,
            'upload_id': '%s_upload' % css_id,
            'thumb_id': "%s_thumbnail_img" % css_id,
            'span_id': "%s_description_txt" % css_id,
            'fileinput_id': "%s_fileinput" % css_id,
            'upload_id': "%s_upload" % css_id,
            'id': css_id,
        }
        html = render_to_string('admin/folderless/file_widget.html', context)
        return mark_safe(html)

    def label_for_value(self, value):
        obj = self.obj_for_value(value)
        return '&nbsp;<strong>%s</strong>' % obj

    def obj_for_value(self, value):
        try:
            key = self.rel.get_related_field().name
            obj = self.rel.to._default_manager.get(**{key: value})
        except:
            obj = None
        return obj

    class Media:
        js = (settings.FOLDERLESS_STATIC_URL +  'js/jquery.iframe-transport.js',)
        js = (settings.FOLDERLESS_STATIC_URL +  'js/jquery.fileupload.js',)
        js = (settings.FOLDERLESS_STATIC_URL +  'js/jquery.folderless_file_widget.js',)


class FolderlessFileFormField(forms.ModelChoiceField):
    widget = FolderlessFileWidget

    def __init__(self, rel, queryset, to_field_name, *args, **kwargs):
        self.rel = rel
        self.queryset = queryset
        self.to_field_name = to_field_name
        self.max_value = None
        self.min_value = None
        kwargs.pop('widget', None)
        forms.Field.__init__(self, widget=self.widget(rel, site), *args, **kwargs)

    def widget_attrs(self, widget):
        widget.required = self.required
        return {}


class FolderlessFileField(models.ForeignKey):
    default_form_class = FolderlessFileFormField
    default_model_class = File

    def __init__(self, **kwargs):
        # we call ForeignKey.__init__ with the File model as parameter.
        return super(FolderlessFileField, self).__init__(
            self.default_model_class, **kwargs)

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {
            'form_class': self.default_form_class,
            'rel': self.rel,
        }
        defaults.update(kwargs)
        return super(FolderlessFileField, self).formfield(**defaults)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.related.ForeignKey"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)
import json

from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.forms.models import modelform_factory

from folderless.utils import handle_upload, UploadException
from folderless.models import File


class FileDateFilter(admin.SimpleListFilter):
    title = _(u'Extension')
    parameter_name = 'original_filename__iendswith'
    def lookups(self,request,model_admin):
        ext_files = File.objects.all().distinct('')
    def queryset (self, request, queryset):
        if self.value() is not None:
            return queryset.filter(original_filename__iendswith=self.value())
        else:
            return queryset

class FileTypeFilter(admin.SimpleListFilter):
    title = _(u'Type')
    parameter_name = 'type__exact'

    def lookups(self, request, model_admin):
        # TODO: limit filter to existing types? distinct ON doesnt work in sqlite3...soo...
        #ext_files = File.objects.all().distinct('extension')
        types = []
        for key, definition in settings.FOLDERLESS_FILE_TYPES.iteritems():
            types.append((key, definition.get("title")))
        return sorted(types, key=lambda type: type[1])

    def queryset (self, request, queryset):
        if self.value() is not None:
            return queryset.filter(type__exact=self.value())
        else:
            return queryset

class FileAdmin(admin.ModelAdmin):
    list_display = ['thumb_list', 'label', 'references_list', 'uploader', 'created', 'modified', ]
    list_filter = [FileTypeFilter, 'created', 'modified', 'extension', 'uploader']
    list_display_links = ['label', ]
    readonly_fields = ['original_filename', 'type', 'extension', 'uploader', 'created', 'modified', 'sha1',]
    search_fields = ['original_filename', 'title', ]

    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            settings.FOLDERLESS_STATIC_URL + 'js/vendor/jquery.ui.widget.js',
            settings.FOLDERLESS_STATIC_URL + 'js/vendor/jquery.iframe-transport.js',
            settings.FOLDERLESS_STATIC_URL + 'js/vendor/jquery.fileupload.js',
             settings.FOLDERLESS_STATIC_URL + "js/jquery.folderless_change_list.js",
        )
        css = {
            'screen': (
                settings.FOLDERLESS_STATIC_URL + "css/folderless.css",
            )
        }

    # TODO: what if used outside of ADMIN?
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploader = request.user
            obj.save()
        super(FileAdmin, self).save_model(request, obj, form, change)

    def get_urls(self):
        from django.conf.urls import patterns, url
        urls = super(FileAdmin, self).get_urls()
        url_patterns = patterns('',
            url(r'^ajax-upload/$',
                self.admin_site.admin_view(self.ajax_upload),
                name='folderless-ajax_upload'),
            url(r'^ajax-info/$',
                self.admin_site.admin_view(self.ajax_info),
                name='folderless-ajax_info'),
        )
        url_patterns.extend(urls)
        return url_patterns

    def ajax_info(self, request):
        file_id = request.GET.get("file_id", None)
        file_obj = get_object_or_404(File, pk=file_id)
        mimetype = "application/json" if request.is_ajax() else "text/html"
        content_type_key = 'content_type' # 'mimetype' if DJANGO_1_4 else 'content_type'
        response_params = {content_type_key: mimetype}
        return HttpResponse(json.dumps(file_obj.get_json_response()),
                            **response_params)

    def ajax_upload(self, request):
        """
        receives an upload from the uploader. Receives only one file at the time.
        """
        mimetype = "application/json" if request.is_ajax() else "text/html"
        content_type_key = 'content_type' # 'mimetype' if DJANGO_1_4 else 'content_type'
        response_params = {content_type_key: mimetype}
        try:
            upload, filename, is_raw = handle_upload(request)
            FileForm = modelform_factory(
                model = File,
                fields = ('original_filename', 'uploader', 'file')
            )
            uploadform = FileForm({'original_filename': filename,
                                   'uploader': request.user.pk},
                                  {'file': upload})
            if uploadform.is_valid():
                file_obj = uploadform.save(commit=False)
                file_obj.save()
                json_response = file_obj.get_json_response()
                return HttpResponse(json.dumps(json_response),
                                    **response_params)
            else:
                form_errors = '; '.join(['%s: %s' % (
                    field,
                    ', '.join(errors)) for field, errors in list(uploadform.errors.items())
                ])
                raise UploadException("AJAX request not valid: form invalid '%s'" % (form_errors,))
        except UploadException as e:
            return HttpResponse(json.dumps({'error': str(e)}),
                                **response_params)


admin.site.register(File, FileAdmin)

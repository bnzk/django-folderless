import json

from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.forms.models import modelform_factory

from folderless.utils import handle_upload, get_valid_filename, UploadException, sha1_from_file
from folderless.models import File
from folderless.forms import FileAdminChangeFrom


class FileDateFilter(admin.SimpleListFilter):
    title = _('Extension')
    parameter_name = 'original_filename__iendswith'

    def lookups(self, request, model_admin):
        ext_files = File.objects.all().distinct('')
        return ext_files

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(original_filename__iendswith=self.value())
        else:
            return queryset


class FileTypeFilter(admin.SimpleListFilter):
    title = _('Type')
    parameter_name = 'type__exact'

    def lookups(self, request, model_admin):
        # TODO: limit filter to existing types?
        # distinct ON doesnt work in sqlite3...soo...
        types = []

        for key, definition in settings.FOLDERLESS_FILE_TYPES.items():
            types.append((key, definition.get("title")))

        return sorted(types, key=lambda type: type[1])

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(type__exact=self.value())
        else:
            return queryset


class FileAdmin(admin.ModelAdmin):
    list_display = [
        'thumb_list', 'label', 'references_list', 'uploader', 'created',
        'modified', ]
    list_filter = [
        FileTypeFilter, 'created', 'modified', 'extension', 'uploader', ]
    list_display_links = ['label', ]
    readonly_fields = [
        'type', 'extension', 'uploader', 'created',
        'modified', 'file_hash', ]
    search_fields = ['filename', 'name', ]

    form = FileAdminChangeFrom

    class Media:
        vendor_path = settings.FOLDERLESS_STATIC_URL + 'js/vendor/'
        js_path = settings.FOLDERLESS_STATIC_URL + 'js/'
        js = (
            vendor_path + 'jquery.ui.widget.js',
            vendor_path + 'jquery.iframe-transport.js',
            vendor_path + 'jquery.fileupload.js',
            'admin/js/jquery.init.js',
            js_path + 'jquery.folderless_change_list.js',
            # js_path + 'jquery_post_init.js',
        )
        css = {
            'screen': (
                settings.FOLDERLESS_STATIC_URL + 'css/folderless.css',
            )
        }

    # TODO: what if used outside of ADMIN?
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploader = request.user
            obj.save()
        super(FileAdmin, self).save_model(request, obj, form, change)

    def get_urls(self):
        from django.conf.urls import url
        urls = super(FileAdmin, self).get_urls()

        url_patterns = [
            url(
                r'^ajax-upload/$',
                self.admin_site.admin_view(self.ajax_upload),
                name='folderless-ajax_upload'
            ),
            url(
                r'^ajax-info/$',
                self.admin_site.admin_view(self.ajax_info),
                name='folderless-ajax_info'
            ),
        ]
        url_patterns.extend(urls)
        return url_patterns

    def ajax_info(self, request):
        file_id = request.GET.get("file_id", None)
        file_obj = get_object_or_404(File, pk=file_id)
        mimetype = "application/json" if request.is_ajax() else "text/html"
        response_params = {'content_type': mimetype}
        return HttpResponse(json.dumps(file_obj.get_json_response()),
                            **response_params)

    def ajax_upload(self, request):
        """
        receives an upload from the uploader.
        Receives only one file at the time.
        """
        mimetype = "application/json" if request.is_ajax() else "text/html"
        content_type_key = 'content_type'
        # 'mimetype' if DJANGO_1_4 else 'content_type'
        response_params = {content_type_key: mimetype}

        try:
            upload, filename, is_raw = handle_upload(request)
            FileForm = modelform_factory(
                model=File, fields=('filename', 'file_hash', 'uploader', 'file'))
            uploadform = FileForm(
                {
                    'filename': get_valid_filename(filename),
                    'file_hash': sha1_from_file(upload),
                    'uploader': request.user.pk
                },
                {'file': upload}
            )

            if uploadform.is_valid():
                file_obj = uploadform.save(commit=False)
                file_obj.save()
                json_response = file_obj.get_json_response()
                return HttpResponse(
                    json.dumps(json_response), **response_params)
            else:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': _(u"Duplicate detected: File with same contents or same name (%(filename)s) already exists. File was not uploaded.") % {'filename': filename, },
                        'errors': uploadform.errors
                    }),
                    status=409,  # conflict
                    **response_params)
        except UploadException as e:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': str(e)
                }),
                **response_params)


admin.site.register(File, FileAdmin)

from django.contrib import admin
from django.conf import settings

from models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ['title', 'original_filename', 'type', 'author', 'uploader', 'created', 'modified', ]
    readonly_fields = ['original_filename', 'type', 'uploader', 'created', 'modified', 'sha1',]
    list_filter = ['type', 'created']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploader = request.user
            obj.save()
        super(FileAdmin, self).save_model(request, obj, form, change)

    class Media:
        css = {
            'screen': (settings.FOLDERLESS_STATIC_URL + "js/popup_handling.js", )
        }


admin.site.register(File, FileAdmin)

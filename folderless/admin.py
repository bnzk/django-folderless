from django.contrib import admin

from models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ['title', 'original_filename', 'type', 'author', 'uploader', 'created', 'modified', ]
    readonly_fields = ['original_filename', 'type', 'uploader', 'created', 'modified', 'sha1',]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploader = request.user
            obj.save()
        super(FileAdmin, self).save_model(request, obj, form, change)

admin.site.register(File, FileAdmin)

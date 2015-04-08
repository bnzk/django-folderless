from django.contrib import admin

from models import TestModel, TestGallery, TestGalleryEntry
from folderless.inlines import FolderlessFileInlineMixin

class TestModelAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", )

admin.site.register(TestModel, TestModelAdmin)



class TestGalleryEntryInline(admin.StackedInline, FolderlessFileInlineMixin):
    model = TestGalleryEntry
    extra = 1


class TestGalleryAdmin(admin.ModelAdmin):
    inlines = [TestGalleryEntryInline, ]

admin.site.register(TestGallery, TestGalleryAdmin)

from django.contrib import admin

from models import TestModel


class TestModelAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", )

admin.site.register(TestModel, TestModelAdmin)

from django.apps import AppConfig


class FolderlessAppConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'folderless'
    verbose_name = 'Folderless File Manager'

from django import forms

from folderless.models import File


# no big deal yet
class FileAdminChangeFrom(forms.ModelForm):
    class Meta:
        model = File
        exclude = []  # ("file_hash", "original_filename")

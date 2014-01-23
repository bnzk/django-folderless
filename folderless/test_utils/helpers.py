#-*- coding: utf-8 -*-
from PIL import Image, ImageChops, ImageDraw

# django-filer inspired.

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User  # NOQA

def create_superuser():
    superuser = User.objects.create_superuser('admin',
                                              'admin@free.fr',
                                              'secret')
    return superuser

def create_image(mode='RGB', size=(800, 600)):
    image = Image.new(mode, size)
    draw = ImageDraw.Draw(image)
    x_bit, y_bit = size[0] // 10, size[1] // 10
    draw.rectangle((x_bit, y_bit * 2, x_bit * 7, y_bit * 3), 'red')
    draw.rectangle((x_bit * 2, y_bit, x_bit * 3, y_bit * 8), 'red')
    return image


class SettingsOverride(object):
    """
    Overrides Django settings within a context and resets them to their inital
    values on exit.

    Example:

        with SettingsOverride(DEBUG=True):
            # do something
    """

    def __init__(self, settings_module, **overrides):
        self.settings_module = settings_module
        self.overrides = overrides

    def __enter__(self):
        self.old = {}
        for key, value in self.overrides.items():
            self.old[key] = getattr(self.settings_module, key, None)
            setattr(self.settings_module, key, value)

    def __exit__(self, _type, value, traceback):
        for key, value in self.old.items():
            if value is not None:
                setattr(self.settings_module, key, value)
            else:
                delattr(self.settings_module, key)
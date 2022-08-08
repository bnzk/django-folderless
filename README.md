# django-folderless

[![CI](https://img.shields.io/github/workflow/status/bnzk/django-folderless/CI.svg?style=flat-square&logo=github "CI")](https://github.com/bnzk/django-folderless/actions/workflows/ci.yml)
[![Version](https://img.shields.io/pypi/v/django-folderless.svg?style=flat-square "Version")](https://pypi.python.org/pypi/django-folderless$/)
[![Licence](https://img.shields.io/github/license/bnzk/django-folderless.svg?style=flat-square "Licence")](https://pypi.python.org/pypi/django-folderless/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/django-folderless?style=flat-square "PyPi Downloads")](https://pypistats.org/packages/django-folderless)


simple media manager for django, folderless.

key features:

- filterable file list with multi upload possibility
- FolderlessFileField, as a replacement for FileField, with instant upload possibility


Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-folderless

Add ``folderless`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'folderless',
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate folderless


Usage
------------

Have a look at the ``folderless/tests/test_app/models.py`` for some example.

.. code-block:: python

    from folderless.fields import FolderlessFileField

    class TestModel(models.Model):
        file = FolderlessFileField(blank=True, null=True)


Contribute
------------

Fork and code. Either run `tox` for complete tests, or `python manage.py test --settings=folderless.tests.settings_test`


Credits / Idea
--------------

main repository: https://github.com/benzkji/django-folderless . many similiar things already exist. no wonder this project is heavily experienced by https://github.com/stefanfoulis/django-filer, and to some extent, feincms.module.medialibrary and https://github.com/samluescher/django-media-tree. initial idea credits: https://github.com/wullerot/ (manipulated django-filer to hide folders completely). more ideas: http://de.slideshare.net/motivesystems/slideshare-upload-gartner-pcc-presentation-going-folderless-with-metadata

this project uses http://semver.org.

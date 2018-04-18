django-folderless
*****************

.. image:: https://travis-ci.org/bnzk/django-folderless.svg
    :target: https://travis-ci.org/bnzk/django-folderless

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

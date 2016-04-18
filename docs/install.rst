.. _installation:

============
Installation
============

Install **django-folderless**. The latest stable release can be found on PyPI.

.. code-block:: bash

	pip install django-folderless

or the newest development version from GitHub

.. code-block:: bash

	pip install -e git+https://github.com/benzkji/django-folderless.git#egg=django-folderless

Basic Configuration
=============

Add ``'folderless'`` to the list of ``INSTALLED_APPS`` in your project's ``settings.py`` file

.. code-block:: python

	INSTALLED_APPS = (
	    ...
	    'folderless',
	    ...
	)

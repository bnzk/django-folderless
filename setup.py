# coding: utf-8
from setuptools import setup, find_packages
import os

version = __import__('folderless').__version__

def read(fname):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-folderless",
    version = version,
    url = 'http://github.com/benzkji/django-folderless',
    license = 'BSD',
    platforms=['OS Independent'],
    description = "folderless media management for django",
    long_description = read('README.rst'),
    author = u'Ben Stähli',
    author_email = 'bnzk@bnzk.ch',
    packages=find_packages(),
    install_requires = (
        # 'Django>=1.3,<1.5',  # no need to limit while in development
        'Django>=1.5',
        'easy-thumbnails>=1.0',
        'django-appconf>=0.6'
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    test_suite='runtests.main',
    tests_require=(
        'argparse',  # needed on python 2.6
    ),
)
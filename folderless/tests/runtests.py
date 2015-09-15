#!/usr/bin/env python
"""
This script is a trick to setup a fake Django environment, since this reusable
app will be developed and tested outside any specifiv Django project.

Via ``settings.configure`` you will be able to set all necessary settings
for your app and run the tests as if you were calling ``./manage.py test``.

"""
import os
import re
import sys

import django
from django.conf import settings

import coverage
from fabric.api import lcd, local  # , abort
from fabric.colors import green, red

import test_settings


if not settings.configured:
    test_settings_dict = test_settings.__dict__
    test_db = os.environ.get('DB', 'sqlite')
    database = test_settings_dict["DATABASES"]["default"]
    if test_db == 'mysql':
        database = {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'folderless_test',
            'USER': 'root',
        }
    elif test_db == 'postgres':
        database = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'NAME': 'folderless_test',
        }
    test_settings_dict.update({
        'DATABASES': {'default': database}
    })
    settings.configure(**test_settings_dict)

django_version = django.get_version()
if '1.7' in django_version or '1.8' in django_version:
    django.setup()

from django_coverage.coverage_runner import CoverageRunner
from django_nose import NoseTestSuiteRunner


class NoseCoverageTestRunner(CoverageRunner, NoseTestSuiteRunner):
    """Custom test runner that uses nose and coverage"""
    def run_tests(self, *args, **kwargs):
        results = super(NoseCoverageTestRunner, self).run_tests(
            *args, **kwargs)
        coverage._the_coverage.data.write_file('.coverage')
        return results


def runtests(*test_args):
    failures = NoseCoverageTestRunner(verbosity=2, interactive=True).run_tests(test_args)

    with lcd(settings.COVERAGE_REPORT_HTML_OUTPUT_DIR):
        total_line = local('grep -n Total index.html', capture=True)
        match = re.search(r'^(\d+):', total_line)
        total_line_number = int(match.groups()[0])
        percentage_line_number = total_line_number + 4
        percentage_line = local(
            'awk NR=={0} index.html'.format(percentage_line_number),
            capture=True)
        match = re.search(r'<td>(\d.+)%</td>', percentage_line)
        percentage = float(match.groups()[0])
    if percentage < 100:
        # abort(red('Coverage is {0}%'.format(percentage)))
        print(red('Coverage is {0}%'.format(percentage)))
    else:
        print(green('Coverage is {0}%'.format(percentage)))

    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])

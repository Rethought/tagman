#!/usr/bin/env python
from django.conf import settings
from django.core.management import call_command


def main():
    """Dynamically configure the Django settings with the
    minimum necessary to get Django running tests"""
    settings.configure(
        INSTALLED_APPS=('tagman', 'django_nose'),
        TEST_RUNNER = 'django_nose.NoseTestSuiteRunner',
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': '/tmp/tagman.db',
                               'USER': '',
                               'PASSWORD': '',
                               'HOST': '',
                               'PORT': ''}}
    )

    # Fire off the tests
    # not getting --with-xunit passed... this is a shame :(
    kwargs = {'with-xunit': ""}
    call_command('test', 'tagman', **kwargs)

if __name__ == '__main__':
    main()

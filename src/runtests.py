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
                               'PORT': ''}},
        NOSE_ARGS=['--with-xunit', '-s'],
    )

    call_command('test', 'tagman')

if __name__ == '__main__':
    main()

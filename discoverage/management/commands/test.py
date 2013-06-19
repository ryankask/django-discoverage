from optparse import make_option

from django.conf import settings
from django.core.management.commands.test import Command as TestCommand


class Command(TestCommand):
    option_list = TestCommand.option_list + (
        make_option(
            '--no-coverage',
            action='store_true',
            dest='no_coverage',
            default=False,
            help='Specifies that no code coverage will be performed.'
        ),
    )

    def handle(self, *args, **kwargs):
        if 'south' in settings.INSTALLED_APPS:
            from south.management.commands import patch_for_test_db_setup
            patch_for_test_db_setup()
        super(Command, self).handle(*args, **kwargs)

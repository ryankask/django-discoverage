from optparse import make_option

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

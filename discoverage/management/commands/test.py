from optparse import make_option

try:
    # TODO: Check if django-discover-runner has overridden the test command
    from discover_runner.management.commands.test import Command as TestCommand
except ImportError:
    from django.core.management.commands.test import Command as TestCommand


class Command(TestCommand):
    option_list = TestCommand.option_list + (
        make_option(
            '--no-coverage',
            action='store_false',
            dest='perform_coverage',
            default=True,
            help='Specifies that no code coverage will be performed.'
        ),
    )

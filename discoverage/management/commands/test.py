from optparse import make_option
from django.core.management import CommandError

try:
    # Depends on a change that will be made on discover runner.
    # It can work without it at the time being and therefor the try...except block exists.
    # Also, even if there was no expected change, it is useful as a foresight.
    from discover_runner.management.commands.test import Command as TestCommand
except ImportError:
    from django.core.management.commands.test import Command as TestCommand

class Command(TestCommand):
    option_list = TestCommand.option_list + (
        make_option('--no-coverage',
            action='store_false', dest='perform_coverage', default=True,
            help='Specifies that no code coverage will be performed.'),
    )
from optparse import make_option
import os
from django.core.management import BaseCommand, CommandError
from discoverage.utils import CoverageHandler

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--filename',
            action='store', dest='filename', default='.coverage',
            help='Specifies the coverage data file to be erased. Defaults to .coverage'),
        )

    def handle(self, filename='.coverage', **options):
        cov = CoverageHandler(data_file=filename)

        if not os.path.exists(filename):
            raise CommandError("'%s' coverage data file does not exist." % filename)

        cov.erase()

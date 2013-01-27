from optparse import make_option
from coverage import coverage
import os
from django.core.management import BaseCommand, CommandError

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--filename',
            action='store', dest='filename', default='.coverage',
            help='Specifies the coverage data file to be erased. Defaults to .coverage'),
        )

    coverage_class = coverage

    def handle(self, filename='.coverage', **options):
        if not os.path.exists(filename):
            raise CommandError("'%s' coverage data file does not exist." % filename)

        cov = self.coverage_class(data_file=filename)

        cov.erase()

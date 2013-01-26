from coverage import coverage
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, filename, **options):
        cov = coverage(data_file=filename)

        cov.erase()

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
        make_option('--data',
            action='store_true', dest='data', default=False,
            help='Specifies that an code coverage report should be produced.'),
        make_option('--data-file',
            action='store', dest='data_file', default=None,
            help='Specifies that file path for which the code coverage report should be produced in. ./.coverage by default'),
        make_option('--html',
            action='store_true', dest='html', default=False,
            help='Specifies that an html report for the code coverage should be produced.'),
        make_option('--xml',
            action='store_true', dest='xml', default=False,
            help='Specifies that an html report for the code coverage should be produced.'),
        make_option('--annotate',
            action='store_true', dest='annotate', default=False,
            help=(
                'Specifies whether coverage should annotate the source code with coverage data (will be placed in a copy of the source code).')),
        make_option('--html-reports-directory',
            action='store', dest='html_reports_directory', default=None,
            help=(
                'Specifies the directory path for which the html code coverage report will be produced in. ./coverage by default')),
        make_option('--xml-reports-file',
            action='store', dest='xml_reports_file', default=None,
            help=(
                'Specifies the file path for which the xml code coverage report will be produced in. ./coverage.xml by default')),
        make_option('--annotate-reports-directory',
            action='store', dest='annotate_reports_directory', default=None,
            help=(
                'Specifies the directory path for which the annotated code coverage report will be produced in. ./coverage by default')),
        make_option('--combine',
            action='store_true', dest='combine', default=False,
            help=(
                'Specifies whether coverage should combine code coverage data from previous runs.')),
        make_option('--branch-coverage',
            action='store_true', dest='branch_coverage', default=False,
            help=(
                'Specifies whether coverage should include branch coverage data.'))
        )

    def handle(self, *test_labels, **options):
        if not options['perform_coverage']:
            if options['data']:
                raise CommandError("Cannot produce a code coverage report when --no-coverage is specified.")

            if options.get('data_file'):
                raise CommandError("Argument --data-file is irrelevant when --no-coverage is specified.")

            if options['html']:
                raise CommandError("Cannot produce an html report when --no-coverage is specified.")

            if options['html_reports_directory']:
                raise CommandError("Argument --html-reports-directory is irrelevant when --no-coverage is specified.")

            if options['xml']:
                raise CommandError("Cannot produce an xml report when --no-coverage is specified.")

            if options['xml_reports_file']:
                raise CommandError("Argument --xml-reports-file is irrelevant when --no-coverage is specified.")

            if options['annotate']:
                raise CommandError('Cannot annotate source code report when --no-coverage is specified.')

            if options['annotate_reports_directory']:
                raise CommandError("Argument --annotate-reports-directory is irrelevant when --no-coverage is specified.")

            if options['branch_coverage']:
                raise CommandError('Cannot cover branches when --no-coverage is specified.')

            if options['combine']:
                raise CommandError('Cannot combine code coverage reports when --no-coverage is specified.')

        if not options['html'] and options['html_reports_directory']:
            raise CommandError("--html must also be specified.")

        if not options['xml'] and options['xml_reports_file']:
            raise CommandError("--xml must also be specified.")

        if not options['data'] and options['data_file']:
            raise CommandError("--data must also be specified.")

        if not options['annotate'] and options['annotate_reports_directory']:
            raise CommandError("--annotate must also be specified.")

        if options['html'] and not options['html_reports_directory']:
            options['html_reports_directory'] = './coverage/'

        if options['xml'] and not options['xml_reports_file']:
            options['xml_reports_file'] = './coverage.xml'

        if options['data'] and not options['data_file']:
            options['data_file'] = './.coverage'

        if options['annotate'] and not options['annotate_reports_directory']:
            options['annotate_reports_directory'] = './coverage/annotate/'

        super(Command, self).handle(*test_labels, **options)
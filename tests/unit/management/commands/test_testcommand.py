from django.core.management import CommandError
from mock import patch
import discoverage
from discoverage.management.commands.test import Command
from tests.testcases import ManagementCommandTestCase

discover_test_command = False

try:
    # Depends on a change that will be made on discover runner.
    # It can work without it at the time being and therefor the try...except block exists.
    # Also, even if there was no expected change, it is useful as a foresight.
    from discover_runner.management.commands.test import Command as TestCommand

    discover_test_command = True
except ImportError:
    from django.core.management.commands.test import Command as TestCommand

class TestCommandTestCase(ManagementCommandTestCase):
    command_options = {
        'interactive': True,
        'failfast': False,
        'testrunner': None,
        'liveserver': None,
        'perform_coverage': True,
        'html': False,
        'html_reports_directory': None,
        'xml': False,
        'xml_reports_file': None,
        'annotate': False,
        'annotate_reports_directory': None,
        'data': False,
        'data_file': None,
        'combine': False,
        'branch_coverage': False
    }

    @classmethod
    def setUpClass(cls):
        if discover_test_command:
            cls.command_options.update({
                'test_discover_root': None,
                'top_level': None,
                'pattern': None
            })

        super(TestCommandTestCase, cls).setUpClass()


class TestCommandParametersFailureTests(TestCommandTestCase):
    def test_that_when_specifying_no_coverage_the_data_argument_cannot_be_specified(self):
        sut = Command()

        options = self.set_command_options(perform_coverage=False, data=True)

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'Cannot produce a code coverage report when --no-coverage is specified.'):
                sut.handle((), **options)

    def test_that_when_specifying_no_coverage_the_annotate_argument_cannot_be_specified(self):
        sut = Command()

        options = self.set_command_options(perform_coverage=False, annotate=True)

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'Cannot annotate source code report when --no-coverage is specified.'):
                sut.handle((), **options)

    def test_that_when_specifying_no_coverage_the_annotate_reports_directory_argument_cannot_be_specified(self):
        sut = Command()

        options = self.set_command_options(perform_coverage=False, annotate_reports_directory='./coverage')

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'Argument --annotate-reports-directory is irrelevant when --no-coverage is specified.'):
                sut.handle((), **options)

    def test_that_when_specifying_no_coverage_the_combine_argument_cannot_be_specified(self):
        sut = Command()

        options = self.set_command_options(perform_coverage=False, combine=True)

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'Cannot combine code coverage reports when --no-coverage is specified.'):
                sut.handle((), **options)

    def test_that_when_specifying_no_coverage_the_branch_coverage_argument_cannot_be_specified(self):
        sut = Command()

        options = self.set_command_options(perform_coverage=False, branch_coverage=True)

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'Cannot cover branches when --no-coverage is specified.'):
                sut.handle((), **options)

    def test_that_when_specifying_no_coverage_the_data_file_argument_cannot_be_specified(self):
        sut = Command()

        options = self.set_command_options(perform_coverage=False, data_file='.coverage')

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'Argument --data-file is irrelevant when --no-coverage is specified.'):
                sut.handle((), **options)

    def test_that_when_specifying_no_coverage_the_html_argument_cannot_be_specified(self):
        sut = Command()

        options = self.set_command_options(perform_coverage=False, html=True)

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'Cannot produce an html report when --no-coverage is specified.'):
                sut.handle((), **options)

    def test_that_when_specifying_no_coverage_the_html_reports_directory_argument_cannot_be_specified(self):
        sut = Command()

        options = self.set_command_options(perform_coverage=False, html_reports_directory='./coverage/')

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'Argument --html-reports-directory is irrelevant when --no-coverage is specified.'):
                sut.handle((), **options)

    def test_that_when_specifying_no_coverage_the_xml_argument_cannot_be_specified(self):
        sut = Command()

        options = self.set_command_options(perform_coverage=False, xml=True)

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'Cannot produce an xml report when --no-coverage is specified.'):
                sut.handle((), **options)

    def test_that_when_specifying_no_coverage_the_xml_reports_file_argument_cannot_be_specified(self):
        sut = Command()

        options = self.set_command_options(perform_coverage=False, xml_reports_file='./coverage.xml')

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'Argument --xml-reports-file is irrelevant when --no-coverage is specified.'):
                sut.handle((), **options)

    def test_that_specifying_the_html_report_directory_argument_without_the_html_argument_is_not_possible(self):
        sut = Command()

        options = self.set_command_options(html_reports_directory='./coverage/')

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'--html must also be specified.'):
                sut.handle((), **options)

    def test_that_specifying_the_xml_report_file_argument_without_the_xml_argument_is_not_possible(self):
        sut = Command()

        options = self.set_command_options(xml_reports_file='./coverage.xml')
        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'--xml must also be specified.'):
                sut.handle((), **options)

    def test_that_specifying_the_data_file_argument_without_the_data_argument_is_not_possible(self):
        sut = Command()

        options = self.set_command_options(data_file='.coverage')

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'--data must also be specified.'):
                sut.handle((), **options)

    def test_that_specifying_the_annotate_reports_directory_argument_without_the_annotate_argument_is_not_possible(
            self):
        sut = Command()

        options = self.set_command_options(annotate_reports_directory='./coverage')

        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0):
            with self.assertRaisesRegexp(CommandError,
                r'--annotate must also be specified.'):
                sut.handle((), **options)


class TestCommandParametersSuccessTests(TestCommandTestCase):
    def test_that_all_arguments_exist(self):
        self.assertAllArgumentsExist(Command)

    def test_that_when_specifying_the_data_argument_without_the_data_file_argument_then_data_file_is_assigned_to_default(
            self):
        with patch('discoverage.runner.DiscoverageRunner', autospec=discoverage.runner.DiscoverageRunner,
            spec_set=True) as test_runner:
            mocked_instance = test_runner.return_value
            mocked_instance.run_tests.return_value = 0
            with patch('django.test.utils.get_runner', return_value=test_runner, spec_set=True):
                options = self.set_command_options(data=True)
                sut = Command()

                sut.handle(*(), **options)

                options = self.set_command_options(data=True, data_file='./.coverage')
                test_runner.assert_called_once_with(*(), **options)

    def test_that_when_specifying_the_html_argument_without_the_html_reports_directory_argument_then_html_reports_directory_argument_is_assigned_to_default(
            self):
        with patch('discoverage.runner.DiscoverageRunner', autospec=discoverage.runner.DiscoverageRunner,
            spec_set=True) as test_runner:
            mocked_instance = test_runner.return_value
            mocked_instance.run_tests.return_value = 0
            with patch('django.test.utils.get_runner', return_value=test_runner, spec_set=True):
                options = self.set_command_options(html=True)
                sut = Command()

                sut.handle(*(), **options)

                options = self.set_command_options(html=True, html_reports_directory='./coverage/')
                test_runner.assert_called_once_with(*(), **options)

    def test_that_when_specifying_the_xml_argument_without_the_xml_reports_file_argument_then_xml_reports_file_is_assigned_to_default(
            self):
        with patch('discoverage.runner.DiscoverageRunner', autospec=discoverage.runner.DiscoverageRunner,
            spec_set=True) as test_runner:
            mocked_instance = test_runner.return_value
            mocked_instance.run_tests.return_value = 0
            with patch('django.test.utils.get_runner', return_value=test_runner, spec_set=True):
                options = self.set_command_options(xml=True)
                sut = Command()

                sut.handle(*(), **options)

                options = self.set_command_options(xml=True, xml_reports_file='./coverage.xml')
                test_runner.assert_called_once_with(*(), **options)

    def test_that_when_specifying_the_annotate_argument_without_the_annotate_reports_directory_argument_then_annotate_reports_directory_is_assigned_to_default(
            self):
        with patch('discoverage.runner.DiscoverageRunner', autospec=discoverage.runner.DiscoverageRunner,
            spec_set=True) as test_runner:
            mocked_instance = test_runner.return_value
            mocked_instance.run_tests.return_value = 0
            with patch('django.test.utils.get_runner', return_value=test_runner, spec_set=True):
                options = self.set_command_options(annotate=True)
                sut = Command()

                sut.handle(*(), **options)

                options = self.set_command_options(annotate=True, annotate_reports_directory='./coverage/annotate/')
                test_runner.assert_called_once_with(*(), **options)


class TestCommandTests(TestCommandTestCase):
    def test_that_the_test_runner_is_invoked_with_all_test_labels(self):
        with patch('discoverage.runner.DiscoverageRunner.run_tests', return_value=0) as run_tests:
            options = self.default_options
            sut = Command()
            expected = ('app.tests', 'otherapp.tests')

            sut.handle(*expected, **options)

            run_tests.assert_called_once_with(expected)
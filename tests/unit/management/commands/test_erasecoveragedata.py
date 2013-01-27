from django.core.management import CommandError
from mock import patch
from discoverage.management.commands.erasecoveragedata import Command
from tests.testcases import ManagementCommandTestCase

class EraseCoverageDataParametersTestCase(ManagementCommandTestCase):
    command_options = {
        'filename': '.coverage'
    }


class EraseCoverageDataParametersFailureTestCase(EraseCoverageDataParametersTestCase):
    def test_that_when_file_does_not_exist_an_error_is_displayed(self):
        sut = Command()
        with patch('os.path.exists', new_callable=lambda: lambda a: False):
            with self.assertRaisesRegexp(CommandError, "'[a-zA-Z0-9\._-]+' coverage data file does not exist."):
                sut.handle()

    def test_that_when_file_does_not_exist_erase_if_never_called(self):
        sut = Command()
        with patch('os.path.exists', new_callable=lambda: lambda a: False), patch('coverage.coverage.erase') as erase:
            try:
                sut.handle()
            except CommandError:
                pass

            self.assertEqual(erase.call_count, 0, 'The command should not erase coverage data')


class EraseCoverageDataCommandParametersSuccessTestCase(EraseCoverageDataParametersTestCase):
    def test_that_all_arguments_exist(self):
        self.assertAllArgumentsExist(Command)

    def test_that_when_file_does_exist_no_error_is_displayed(self):
        sut = Command()
        with patch('os.path.exists', new_callable=lambda: lambda a: True), patch('coverage.coverage.erase'):
            try:
                sut.handle()
            except Exception, e:
                self.fail(e.message)


class EraseCoverageDataCommandTests(EraseCoverageDataParametersTestCase):
    def test_that_when_a_filename_is_not_specified_and_the_default_file_exists_then_the_file_name_is_passed_to_the_coverage_object4(
            self):
        sut = Command()
        with patch('os.path.exists', new_callable=lambda: lambda a: True), patch('coverage.coverage',
            autospec=True) as cov:
            sut.coverage_class = cov

            sut.handle()

            cov.assert_called_once_with(data_file='.coverage')

    def test_that_when_a_filename_is_specified_and_the_file_exists_then_the_file_name_is_passed_to_the_coverage_object4(
            self):
        sut = Command()

        options = self.set_command_options(filename='.someotherfile')
        with patch('os.path.exists', new_callable=lambda: lambda a: True), patch('coverage.coverage',
            autospec=True) as cov:
            sut.coverage_class = cov

            sut.handle(**options)

            cov.assert_called_once_with(data_file='.someotherfile')

    def test_that_when_file_exists_erase_is_called(self):
        sut = Command()
        with patch('os.path.exists', new_callable=lambda: lambda a: True), patch('coverage.coverage.erase') as erase:
            sut.handle()

            erase.assert_called_once_with()

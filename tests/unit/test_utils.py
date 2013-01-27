from mock import patch, ANY, call
from discoverage.settings import COVERAGE_OMIT_MODULES, COVERAGE_EXCLUDE_PATTERNS
from discoverage.utils import CoverageHandler
from tests.testcases import CoverageHandlerTestCase

@patch('coverage.coverage', autospec=True, spec_set=True)
class CoverageHandlerInitializationArgumentsSuccessTests(CoverageHandlerTestCase):
    def test_that_when_the_omit_argument_is_not_supplied_it_is_equal_to_the_coverage_omit_modules_setting(self, cov):
        CoverageHandler()

        cov.assert_called_once_with(omit=COVERAGE_OMIT_MODULES, data_file=ANY, branch=ANY)

    def test_that_when_the_data_file_argument_is_not_supplied_it_is_equal_to_none(self, cov):
        CoverageHandler()

        cov.assert_called_once_with(omit=ANY, data_file=None, branch=ANY)

    def test_that_when_the_branch_coverage_argument_is_not_supplied_it_is_equal_to_false(self, cov):
        CoverageHandler()

        cov.assert_called_once_with(omit=ANY, data_file=ANY, branch=False)

    @patch('coverage.coverage.exclude', autospec=True, spec_set=True)
    def test_that_when_the_exclude_patterns_argument_is_not_supplied_it_is_equal_to_the_coverage_exclude_patterns_setting(
            self, cov, exclude):
        CoverageHandler()

        exclude.assert_has_calls([call().exclude(pattern) for pattern in COVERAGE_EXCLUDE_PATTERNS])

    def test_that_when_the_html_argument_is_not_supplied_it_is_equal_to_false(self, cov):
        sut = CoverageHandler()

        self.assertFalse(sut.html)

    def test_that_when_the_html_reports_directory_argument_is_not_supplied_it_is_equal_to_none(self, cov):
        sut = CoverageHandler()

        self.assertIsNone(sut.html_reports_directory)

    def test_that_when_the_xml_argument_is_not_supplied_it_is_equal_to_false(self, cov):
        sut = CoverageHandler()

        self.assertFalse(sut.xml)

    def test_that_when_the_xml_reports_file_argument_is_not_supplied_it_is_equal_to_none(self, cov):
        sut = CoverageHandler()

        self.assertIsNone(sut.xml_reports_file)

    def test_that_when_the_annotate_argument_is_not_supplied_it_is_equal_to_false(self, cov):
        sut = CoverageHandler()

        self.assertFalse(sut.annotate)

    def test_that_when_the_annotate_reports_directory_argument_is_not_supplied_it_is_equal_to_none(self, cov):
        sut = CoverageHandler()

        self.assertIsNone(sut.annotate_reports_directory)

    def test_that_when_the_combine_argument_is_not_supplied_it_is_equal_to_false(self, cov):
        sut = CoverageHandler()

        self.assertFalse(sut.combine)

    def test_that_when_the_branch_coverage_argument_is_not_supplied_it_is_equal_to_false(self, cov):
        sut = CoverageHandler()

        self.assertFalse(sut.branch_coverage)

@patch('coverage.coverage.start', autospec=True, spec_set=True)
class StartTests(CoverageHandlerTestCase):
    def test_that_when_invoking_start_the_coverage_start_method_is_called(self, start):
        sut = CoverageHandler()
        sut.start()
        start.assert_called_once_with(sut.cov)
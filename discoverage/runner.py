from discover_runner import DiscoverRunner
from discoverage.utils import CoverageHandler

class DiscoverageRunner(DiscoverRunner):
    def __init__(self, perform_coverage=True,
                 html=False,
                 html_reports_directory=None,
                 xml=False,
                 xml_reports_file=None,
                 annotate=False,
                 annotate_reports_directory=None,
                 data=False,
                 data_file=None,
                 combine=False,
                 branch_coverage=False, **kwargs):
        self.perform_coverage = perform_coverage

        self.coverage_handler = CoverageHandler(html=html,
            html_reports_directory=html_reports_directory,
            xml=xml,
            xml_reports_file=xml_reports_file,
            annotate=annotate,
            annotate_reports_directory=annotate_reports_directory,
            data=data,
            data_file=data_file,
            combine=combine,
            branch_coverage=branch_coverage)

        super(DiscoverageRunner, self).__init__(**kwargs)

    def build_suite(self, *args, **kwargs):
        if not hasattr(self, '_suite'):
            self._suite = super(DiscoverageRunner, self).build_suite(
                *args, **kwargs)
        return self._suite

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        if not self.perform_coverage:
            return super(DiscoverageRunner, self).run_tests(test_labels, extra_tests=extra_tests, **kwargs)

        self.coverage_handler.start()

        result = super(DiscoverageRunner, self).run_tests(
            test_labels, extra_tests, **kwargs)

        self.coverage_handler.stop()

        suite = self.build_suite(test_labels, extra_tests)

        self.coverage_handler.report(suite)

        return result

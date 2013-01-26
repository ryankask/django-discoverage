import coverage
from discover_runner import DiscoverRunner

from discoverage.settings import COVERAGE_OMIT_MODULES, COVERAGE_EXCLUDE_PATTERNS, MODULE_NAME_DISCOVERY_PATTERN, MODULE_NAME_APP_DISCOVERY, PKG_NAME_APP_DISCOVERY
from discoverage.utils import find_coverage_apps, get_all_modules, CoverageHandler


class DiscoverageRunner(DiscoverRunner):
    def __init__(self, perform_coverage=True, **kwargs):
        self.perform_coverage = perform_coverage

        super(DiscoverageRunner, self).__init__(**kwargs)

    def build_suite(self, *args, **kwargs):
        if not hasattr(self, '_suite'):
            self._suite = super(DiscoverageRunner, self).build_suite(
                *args, **kwargs)
        return self._suite

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        if not self.perform_coverage:
            return super(DiscoverageRunner, self).run_tests(test_labels, extra_tests=extra_tests, **kwargs)
        suite = self.build_suite(test_labels, extra_tests)

        coverage = CoverageHandler(suite, COVERAGE_OMIT_MODULES,
            COVERAGE_EXCLUDE_PATTERNS,
            MODULE_NAME_APP_DISCOVERY,
            MODULE_NAME_DISCOVERY_PATTERN,
            PKG_NAME_APP_DISCOVERY)
        with coverage:
            result = super(DiscoverageRunner, self).run_tests(
                test_labels, extra_tests, **kwargs)

        return result

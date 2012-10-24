import coverage
from discover_runner import DiscoverRunner

from discoverage.settings import OMIT_MODULES, APPS_TEST_CASE_ATTR

def find_coverage_apps(suite):
    coverage_apps = set()
    for test in suite:
        apps = getattr(test, APPS_TEST_CASE_ATTR, ())
        for app in apps:
            coverage_apps.add(app)
    return coverage_apps


class DiscoverageRunner(DiscoverRunner):
    def build_suite(self, *args, **kwargs):
        if not hasattr(self, '_suite'):
            self._suite = super(DiscoverageRunner, self).build_suite(
                *args, **kwargs)
        return self._suite

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        suite = self.build_suite(test_labels, extra_tests)
        coverage_modules = find_coverage_apps(suite)
        cov = coverage.coverage(source=coverage_modules, omit=OMIT_MODULES)
        cov.start()
        result = super(DiscoverageRunner, self).run_tests(test_labels,
                                                          extra_tests=None,
                                                          **kwargs)
        cov.stop()
        print
        cov.report()
        return result

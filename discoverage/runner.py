import coverage
from django.core.exceptions import ImproperlyConfigured

try:
    from discover_runner import DiscoverRunner
except (ImportError, ImproperlyConfigured):
    from django.test.runner import DiscoverRunner

from discoverage.settings import (COVERAGE_OMIT_MODULES,
                                  COVERAGE_EXCLUDE_PATTERNS)
from discoverage.utils import find_coverage_apps, get_all_modules


class DiscoverageRunner(DiscoverRunner):
    def __init__(self, no_coverage=False, **kwargs):
        self.no_coverage = no_coverage
        super(DiscoverageRunner, self).__init__(**kwargs)

    def build_suite(self, *args, **kwargs):
        if not hasattr(self, '_suite'):
            self._suite = super(DiscoverageRunner, self).build_suite(
                *args, **kwargs)
        return self._suite

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        if self.no_coverage:
            return super(DiscoverageRunner, self).run_tests(
                test_labels, extra_tests=extra_tests, **kwargs)

        cov = coverage.coverage(omit=COVERAGE_OMIT_MODULES)

        for pattern in COVERAGE_EXCLUDE_PATTERNS:
            cov.exclude(pattern)

        cov.start()

        result = super(DiscoverageRunner, self).run_tests(
            test_labels, extra_tests, **kwargs)

        cov.stop()

        suite = self.build_suite(test_labels, extra_tests)
        apps = find_coverage_apps(suite)
        app_modules = get_all_modules(apps)

        if app_modules:
            print
            cov.report(app_modules)

        return result

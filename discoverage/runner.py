import coverage
from discover_runner import DiscoverRunner

from discoverage.settings import OMIT_MODULES
from discoverage.utils import find_coverage_apps, get_all_modules


class DiscoverageRunner(DiscoverRunner):
    def build_suite(self, *args, **kwargs):
        if not hasattr(self, '_suite'):
            self._suite = super(DiscoverageRunner, self).build_suite(
                *args, **kwargs)
        return self._suite

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        cov = coverage.coverage(omit=OMIT_MODULES)
        cov.start()
        result = super(DiscoverageRunner, self).run_tests(test_labels,
                                                          extra_tests,
                                                          **kwargs)
        cov.stop()

        suite = self.build_suite(test_labels, extra_tests)
        apps = find_coverage_apps(suite)
        app_modules = get_all_modules(apps)

        if app_modules:
            print
            cov.report(app_modules)

        return result

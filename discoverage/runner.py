import coverage
from django_coverage.utils.module_tools import get_all_modules
from discover_runner import DiscoverRunner

from discoverage.settings import OMIT_MODULES, APPS_TEST_CASE_ATTR

def find_coverage_apps(suite):
    coverage_apps = set()
    for test in suite:
        apps = getattr(test, APPS_TEST_CASE_ATTR, ())
        for app in apps:
            coverage_apps.add(app)
    return list(coverage_apps)


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
                                                          extra_tests=None,
                                                          **kwargs)
        cov.stop()

        suite = self.build_suite(test_labels, extra_tests)
        apps = find_coverage_apps(suite)
        module_data = get_all_modules(apps, [], [])
        print
        cov.report(module_data[1].values())

        return result

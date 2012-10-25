import coverage
from django.utils.importlib import import_module
from discover_runner import DiscoverRunner
from pkgutil import walk_packages

from discoverage.settings import OMIT_MODULES, APPS_TEST_CASE_ATTR

def get_apps(obj):
    return list(getattr(obj, APPS_TEST_CASE_ATTR, []))

def find_coverage_apps(suite):
    coverage_apps = set()
    inspected_modules = set()

    for test in suite:
        test_apps = get_apps(test)

        if test.__module__ not in inspected_modules:
            test_module = import_module(test.__module__)
            test_apps.extend(get_apps(test_module))
            inspected_modules.add(test.__module__)

            if test_module.__package__ not in inspected_modules:
                test_package = import_module(test_module.__package__)
                test_apps.extend(get_apps(test_package))
                inspected_modules.add(test_module.__package__)

        coverage_apps.update(test_apps)

    return list(coverage_apps)

def get_all_modules(apps):
    modules = set()

    for app in apps:
        app_module = import_module(app)
        modules.add(app_module)
        app_path = app_module.__path__

        for pkg_data in walk_packages(app_path, prefix=u'{0}.'.format(app)):
            current_module = import_module(pkg_data[1])
            modules.add(current_module)

    return list(modules)


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
        app_modules = get_all_modules(apps)
        print
        cov.report(app_modules)

        return result

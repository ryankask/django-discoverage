from coverage import coverage
import re

from django.conf import settings
from django.utils.importlib import import_module
from pkgutil import walk_packages

from discoverage.settings import TESTED_APPS_VAR_NAME

class CoverageHandler(coverage):
    def __init__(self, suite, omit, excluded_patterns, module_name_app_discovery, module_name_discovery_pattern,
                 pkg_name_app_discovery):
        super(CoverageHandler, self).__init__(omit=omit)
        self.suite = suite
        self.module_name_discovery_pattern = module_name_discovery_pattern
        self.module_name_app_discovery = module_name_app_discovery
        self.pkg_name_app_discovery = pkg_name_app_discovery

        for pattern in excluded_patterns:
            self.exclude(pattern)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

        apps = self.find_coverage_apps()
        app_modules = self.get_all_modules(apps)

        self.actual_coverage_percent = self.report(app_modules)

    def get_apps(self, obj):
        return list(getattr(obj, TESTED_APPS_VAR_NAME, []))

    def find_coverage_apps(self):
        coverage_apps = set()
        inspected = set()
        app_pkgs = dict((app.split('.')[-1], app) for app in settings.INSTALLED_APPS)

        for test in self.suite:
            class_name = repr(test.__class__)

            if class_name in inspected:
                continue

            test_apps = self.get_apps(test)

            if test.__module__ not in inspected:
                test_module = import_module(test.__module__)
                test_apps.extend(self.get_apps(test_module))
                inspected.add(test.__module__)
                pkg = test_module.__package__

                if self.module_name_app_discovery:
                    module_name = test.__module__.split(pkg + '.')[-1]

                    try:
                        guessed_app_name = re.match(self.module_name_discovery_pattern,
                            module_name).group(1)
                        test_apps.append(app_pkgs[guessed_app_name])
                    except (KeyError, AttributeError, IndexError):
                        pass

                if pkg not in inspected:
                    test_pkg = import_module(pkg)
                    test_apps.extend(self.get_apps(test_pkg))
                    inspected.add(pkg)

                    if self.pkg_name_app_discovery:
                        subpkg = pkg.split('.')[-1]
                        try:
                            test_apps.append(app_pkgs[subpkg])
                        except KeyError:
                            pass

            inspected.add(class_name)
            coverage_apps.update(test_apps)

        return list(coverage_apps)

    def get_all_modules(self, apps):
        modules = set()

        for app in apps:
            app_module = import_module(app)
            modules.add(app_module)
            app_path = app_module.__path__

            for pkg_data in walk_packages(app_path, prefix=u'{0}.'.format(app)):
                current_module = import_module(pkg_data[1])
                modules.add(current_module)

        return list(modules)

    def report(self, app_modules):
        return super(CoverageHandler, self).report(app_modules)

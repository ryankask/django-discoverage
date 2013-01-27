import coverage
import re

from django.conf import settings
from django.utils.importlib import import_module
from pkgutil import walk_packages

from discoverage.settings import (TESTED_APPS_VAR_NAME, PKG_NAME_APP_DISCOVERY,
                                  MODULE_NAME_APP_DISCOVERY,
                                  MODULE_NAME_DISCOVERY_PATTERN, COVERAGE_OMIT_MODULES, COVERAGE_EXCLUDE_PATTERNS)

class CoverageHandler(object):
    def __init__(self,
                 omit=COVERAGE_OMIT_MODULES,
                 exclude_patterns=COVERAGE_EXCLUDE_PATTERNS,
                 module_name_discovery_pattern=MODULE_NAME_DISCOVERY_PATTERN,
                 module_name_app_discovery=MODULE_NAME_APP_DISCOVERY,
                 package_name_app_discovery=PKG_NAME_APP_DISCOVERY,
                 html=False,
                 html_reports_directory=None,
                 xml=False,
                 xml_reports_file=None,
                 annotate=False,
                 annotate_reports_directory=None,
                 data=False,
                 data_file=None,
                 combine=False,
                 branch_coverage=False):
        self.cov = coverage.coverage(omit=omit, data_file=data_file, branch=branch_coverage)

        for pattern in exclude_patterns:
            self.cov.exclude(pattern)

        self.html = html
        self.html_reports_directory = html_reports_directory
        self.xml = xml
        self.xml_reports_file = xml_reports_file
        self.annotate = annotate
        self.combine = combine
        self.branch_coverage = branch_coverage
        self.annotate_reports_directory = annotate_reports_directory
        self.data = data
        self.module_name_discovery_pattern = module_name_discovery_pattern
        self.module_name_app_discovery = module_name_app_discovery
        self.package_name_app_discovery = package_name_app_discovery

    def start(self):
        self.cov.start()

    def stop(self):
        self.cov.stop()

    def report(self, suite):
        apps = self.find_coverage_apps(suite)
        app_modules = self.get_all_modules(apps)

        if app_modules:
            self.cov.report(app_modules)

            if self.data:
                self.cov.save()

            if self.html:
                self.cov.html_report(morfs=app_modules, directory=self.html_reports_directory)

            if self.xml:
                self.cov.xml_report(morfs=app_modules, outfile=self.xml_reports_file)

            if self.annotate:
                self.cov.annotate(morfs=app_modules, directory=self.annotate_reports_directory)

    def get_apps(self, obj):
        return list(getattr(obj, TESTED_APPS_VAR_NAME, []))


    def find_coverage_apps(self, suite):
        coverage_apps = set()
        inspected = set()
        app_pkgs = dict((app.split('.')[-1], app) for app in settings.INSTALLED_APPS)

        for test in suite:
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

                    if self.package_name_app_discovery:
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

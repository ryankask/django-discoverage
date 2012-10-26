import re

from django.conf import settings
from django.utils.importlib import import_module
from pkgutil import walk_packages

from discoverage.settings import (TESTED_APPS_VAR_NAME, PKG_NAME_APP_DISCOVERY,
                                  MODULE_NAME_APP_DISCOVERY,
                                  MODULE_NAME_DISCOVERY_PATTERN)

def get_apps(obj):
    return list(getattr(obj, TESTED_APPS_VAR_NAME, []))

def find_coverage_apps(suite):
    coverage_apps = set()
    inspected = set()
    app_pkgs = dict((app.split('.')[-1], app) for app in settings.INSTALLED_APPS)

    for test in suite:
        class_name = repr(test.__class__)

        if class_name in inspected:
            continue

        test_apps = get_apps(test)

        if test.__module__ not in inspected:
            test_module = import_module(test.__module__)
            test_apps.extend(get_apps(test_module))
            inspected.add(test.__module__)
            pkg = test_module.__package__

            if MODULE_NAME_APP_DISCOVERY:
                module_name = test.__module__.split(pkg + '.')[-1]

                try:
                    guessed_app_name = re.match(MODULE_NAME_DISCOVERY_PATTERN,
                                                module_name).group(1)
                    test_apps.append(app_pkgs[guessed_app_name])
                except (KeyError, AttributeError, IndexError):
                    pass

            if pkg not in inspected:
                test_pkg = import_module(pkg)
                test_apps.extend(get_apps(test_pkg))
                inspected.add(pkg)

                if PKG_NAME_APP_DISCOVERY:
                    subpkg = pkg.split('.')[-1]
                    try:
                        test_apps.append(app_pkgs[subpkg])
                    except KeyError:
                        pass

        inspected.add(class_name)
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

from django.conf import settings

# The name of the iterable ``django-discoverage`` looks for in the discovery
# process
TESTED_APPS_VAR_NAME = getattr(settings, 'TESTED_APPS_VAR_NAME', 'TESTS_APPS')

# Modules not to trace
OMIT_MODULES = getattr(settings, 'OMIT_MODULES', ['*test*'])

# Determines whether the apps to be included in the coverage report
# should be inferred from the test's subpackage name
PKG_NAME_APP_DISCOVERY = getattr(settings, 'PKG_NAME_APP_DISCOVERY', True)

# Determines whether tested apps are guessed from module names
MODULE_NAME_APP_DISCOVERY = getattr(settings, 'MODULE_NAME_APP_DISCOVERY', False)
MODULE_NAME_DISCOVERY_PATTERN = getattr(settings, 'MODULE_NAME_DISCOVERY_PATTERN',
                                        r'test_?(\w+)')

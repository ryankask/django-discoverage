from django.conf import settings

# The name of the iterable ``django-discoverage`` looks for in the discovery
# process
TESTED_APPS_VAR_NAME = getattr(settings, 'TESTED_APPS_VAR_NAME', 'TESTS_APPS')

# Coverage settings
COVERAGE_OMIT_MODULES = getattr(settings, 'COVERAGE_OMIT_MODULES', ['*test*'])
COVERAGE_EXCLUDE_PATTERNS = getattr(settings, 'COVERAGE_EXCLUDE_PATTERNS', [
    r'def __unicode__\(self\):',
    r'def __str__\(self\):',
    r'def get_absolute_url\(self\):',
    r'from .* import .*',
    r'import .*',
])

# Determines whether the apps to be included in the coverage report
# should be inferred from the test's subpackage name
PKG_NAME_APP_DISCOVERY = getattr(settings, 'PKG_NAME_APP_DISCOVERY', True)

# Determines whether tested apps are guessed from module names
MODULE_NAME_APP_DISCOVERY = getattr(settings, 'MODULE_NAME_APP_DISCOVERY', False)
MODULE_NAME_DISCOVERY_PATTERN = getattr(settings, 'MODULE_NAME_DISCOVERY_PATTERN',
                                        r'test_?(\w+)')

from django.conf import settings

# The attriute on each test case that determines which apps to trace
APPS_TEST_CASE_ATTR = getattr(settings, 'APPS_TEST_CASE_ATTR', 'TESTS_APPS')

# Modules not to trace
OMIT_MODULES = getattr(settings, 'OMIT_MODULES', ['*test*'])

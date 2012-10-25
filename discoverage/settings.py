from django.conf import settings

# The name of the iterable ``django-discoverage`` looks for in the discovery
# process
TESTED_APPS_VAR_NAME = getattr(settings, 'TESTED_APPS_VAR_NAME', 'TESTS_APPS')

# Modules not to trace
OMIT_MODULES = getattr(settings, 'OMIT_MODULES', ['*test*'])

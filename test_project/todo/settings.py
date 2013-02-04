import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                             os.pardir))
sys.path.insert(0, os.path.realpath(os.path.join(PROJECT_ROOT, 'apps')))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
TIME_ZONE = 'US/Eastern'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = True
SECRET_KEY = 'kb49%pkd#-@65w=wpr($vsi0omg%-%ob9u#8w@aiu+wyqt$td7'
WSGI_APPLICATION = 'todo.wsgi.application'

# Next to each installed app is the reason why it was included in the report
INSTALLED_APPS = (
    'accounts', # Package name app discovery
    'todo.notes', # Package name app discovery
    'registration', # In tests.accounts.test_registration.UtilsTests.TESTS_APPS
    'bookmarks', # In tests.notes.test_bookmarks.TESTS_APPS
    'links', # In tests.notes.TESTS_APPS
    'event', # Module name app discovery
    'planner',
)

TEST_RUNNER = 'discoverage.DiscoverageRunner'
TEST_DISCOVER_TOP_LEVEL = TEST_DISCOVER_ROOT = PROJECT_ROOT
MODULE_NAME_APP_DISCOVERY = True

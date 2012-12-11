django-discoverage
==================

Adds `coverage <http://nedbatchelder.com/code/coverage/>`_ to Carl Meyer and
Jannis Leidel's `django-discover-runner
<https://github.com/jezdez/django-discover-runner>`_.

Inspired by `django-coverage <https://bitbucket.org/kmike/django-coverage/>`_.

Usage
-----

One of the objectives of ``django-discover-runner`` is to allow the separation
of a Django app's tests from the code it's testing. Since tests no longer reside
in an app, ``django-discoverage`` needs a different way to know which apps to
include in the coverage report. The runner does this in two ways which are
discussed below.

First, it tries to infer which apps you are testing from the name of the package
in which the test's module lives. For example, if you have an app ``blog`` and
you test the view of the app in the module ``tests.blog.test_views``, the app
will be included in the coverage report. The same happens if the app is a
subpackage and appears in ``INSTALLED_APPS`` as ``myproject.blog``.

This behavior is controlled by the ``PKG_NAME_APP_DISCOVERY`` setting.

Although not on by default, tested apps can also be guessed from the name of the
test's module. For example, if ``MODULE_NAME_APP_DISCOVERY`` is ``True`` and
there is a module named ``tests.test_blog``, the ``blog`` app will be included
in the report. You can override the regular expression used to extract the app
name using the ``MODULE_NAME_DISCOVERY_PATTERN`` setting.

The second way in which ``django-discoverage`` finds apps is by looking for an
iterable of app names (named by default ``TESTS_APPS``) in three places:

1. On a ``TestCase`` instance in the suite.
2. In the ``TestCase`` subclass's module (``test*.py`` by default).
3. In the ``TestCase`` subclass's immediate package. If ``MyTestCase`` is in the
   package ``tests.myapp.test_views``, the runner inspects ``tests.myapp``. It
   does not currently traverse parent packages.

Let's say you had the following test module, ``tests.blog.test_views``::

    TESTS_APPS = ('blog',)

    class MyTestCase(TestCase):
        TESTS_APPS = ('mycoolapp', 'myproject.anothercoolapp')
        ...

All modules in the apps ``blog``, ``mycoolapp``, and
``myproject.anothercoolapp`` will be included in the report along with any apps
listed in ``test.blog.TESTS_APPS``.

Modules specified in ``OMIT_MODULES`` will *not*, however, appear in the report.

Settings
--------

``PKG_NAME_APP_DISCOVERY``
  Determines whether tested apps are guessed from a test module's package
  name. It is on by default.

``MODULE_NAME_APP_DISCOVERY``
  Determines whether tested apps are guessed from a test module's name.

``MODULE_NAME_DISCOVERY_PATTERN``
  A regular expression with a single capturing group that extracts the app name
  from a module name (e.g. "blog" from ``test_blog``). Defaults to
  ``"test_?(\w+)"``.

``TESTED_APPS_VAR_NAME``
  The name of the iterable ``django-discoverage`` looks for in the three places
  listed above. Defaults to ``TESTS_APPS``.

``COVERAGE_OMIT_MODULES``
  Modules not to be traced by ``coverage``. See the `coverage API
  documentation`_ for more details. Defaults to ``['*test*']``.

``COVERAGE_EXCLUDE_PATTERNS``
  A list of of regular expressions that impact coverage reporting. If a line of
  tested code matches one of the patterns in the list, it will not count as a
  missed line. See the `coverage API documentation`_ for more details.

  Defaults to:

  * ``def get_absolute_url(self):``
  * ``def __unicode__(self):``
  * ``def __str__(self):``
  * Any statement with ``import *`` in it

.. _Coverage API documentation: http://nedbatchelder.com/code/coverage/api.html#coverage.coverage

django-discoverage
==================

Adds `coverage <http://nedbatchelder.com/code/coverage/>`_ to Django 1.6's test
runner and Carl Meyer and Jannis Leidel's `django-discover-runner
<https://github.com/jezdez/django-discover-runner>`_.

Inspired by `django-coverage <https://bitbucket.org/kmike/django-coverage/>`_.

django-discoverage works with Django 1.4 and above. If you are using Django 1.4
or 1.5, django-discover-runner is required and will be automatically
installed. That package backports the implementation of ``DiscoverRunner``
included in Django 1.6.

Quick usage
-----------

To run the tests, type:

    ./manage.py test [options] [appname ...]

To run the tests without code coverage (i.e. run ``django-discover-runner``
instead), type:

    ./manage.py test --no-coverage [options] [appname ...]

If you want to use the ``--no-coverage`` option, make sure you add
``discoverage`` to your ``INSTALLED_APPS``.

Detailed usage
--------------

One of the objectives of Django's ``DiscoverRunner`` (previously
``django-discover-runner``) is to allow the separation of a Django app's tests
from the code it's testing. Since tests no longer reside in an app,
``django-discoverage`` needs a different way to know which apps to include in
the coverage report. The runner does this in two ways which are discussed below.

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
  A list of regular expressions that impact coverage reporting. If a line of
  tested code matches one of the patterns in the list, it will not count as a
  missed line. See the `coverage API documentation`_ for more details.

  Defaults to:

  * ``def get_absolute_url(self):``
  * ``def __unicode__(self):``
  * ``def __str__(self):``
  * Any statement with ``import *`` in it

.. _Coverage API documentation: http://nedbatchelder.com/code/coverage/api.html#coverage.coverage

Change Log
----------

1.0.0 (2013-08-27)
~~~~~~~~~~~~~~~~~~

* Handle ``ImproperlyConfigured`` exception raised by ``django-discover-runner``
* The runner is now successfully used in several projects so it's moving to 1.0.

0.7.2 (2013-06-19)
~~~~~~~~~~~~~~~~~~

* Require django-discover-runner 1.0 which now backports Django 1.6's
  implementation of ``DiscoverRunner``.

0.7.1 (2013-06-18)
~~~~~~~~~~~~~~~~~~

* Only install django-discover-runner if the version of Django installed is
  lower than 1.6

0.7.0 (2013-06-05)
~~~~~~~~~~~~~~~~~~

* Support for Django 1.6 and its implementation of
  `DiscoverRunner <https://docs.djangoproject.com/en/dev/topics/testing/advanced/#django.test.runner.DiscoverRunner>`_.

0.6.2 (2013-03-13)
~~~~~~~~~~~~~~~~~~

* Change the default of ``COVERAGE_OMIT_MODULES`` back to ``['*test*']``

0.6.1 (2013-03-06)
~~~~~~~~~~~~~~~~~~

* Include South's test database patching

0.6.0 (2013-02-05)
~~~~~~~~~~~~~~~~~~

* Python 3 support
* Test suite for app discovery methods
* ``--no-coverage`` option

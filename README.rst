django-discoverage
==================

Adds `coverage <http://nedbatchelder.com/code/coverage/>`_ to Jannis Leidel and
Carl Meyer's `django-discover-runner
<https://github.com/jezdez/django-discover-runner>`_.

Inspired by `django-coverage <https://bitbucket.org/kmike/django-coverage/>`_.

Usage
-----

One of the objectives of ``django-discover-runner`` is to allow separating a
Django app's tests from the code it's testing. Since tests no longer reside in
an app, ``django-discoverage`` needs a different way to know which apps to
include in the coverage report. It currently collects apps (packages) by looking
for an iterable (named by default ``TESTS_APPS``) in three places:

1. On a ``TestCase`` instance in the suite.
2. In the ``TestCase`` subclass's module (``test_*.py`` by default).
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
``test.blog.TESTS_APPS``.

Modules specified in ``OMIT_MODULES`` will *not*, however, appear in the report.

Settings
--------

``APPS_TEST_CASE_ATTR``
  The attribute ``django-discoverage`` looks for on each ``TestCase`` instance.

``OMIT_MODULES``
  Modules not to be traced by ``coverage``. See the `coverage API
  documentation
  <http://nedbatchelder.com/code/coverage/api.html#coverage.coverage>`_ for more
  details.

TODO
----

* Investigate discovering the apps being tested from the test modules imports
  (this could be really annoying)

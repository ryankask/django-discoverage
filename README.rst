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
for an attribute (by default ``TESTS_APPS``) on each ``TestCase`` instance in
the suite.

For example::

    class MyTestCase(TestCase):
        TESTS_APPS = ('mycoolapp', 'myproject.anothercoolapp')
        ...

All modules in the listed apps (except those specified in ``OMIT_MODULES``) will
appear in the standard ``coverage`` report.

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
* Check whether the report can be customized to display package names instead of
  paths

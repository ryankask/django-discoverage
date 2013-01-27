from django.test import TestCase

class TestRunnerTestCase(TestCase):
    TESTS_APPS = ['discoverage']

class CoverageHandlerTestCase(TestCase):
    TESTS_APPS = ['discoverage']

class ManagementCommandTestCase(TestCase):
    TESTS_APPS = ['discoverage.management']

    default_options = {
        'settings': None,
        'pythonpath': None,
        'traceback': False,
        'verbosity': 1,
    }

    command_options = {}

    def set_command_options(self, **kwargs):
        options = {}
        options.update(self.default_options)
        options.update(kwargs)

        return options

    @classmethod
    def setUpClass(cls):
        cls.default_options.update(cls.command_options)

    def assertAllArgumentsExist(self, command):
        sut = [option.dest for option in command.option_list]

        self.assertEqual(sut.sort(), self.command_options.keys().sort())
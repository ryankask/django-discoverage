#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

from django.core.management import execute_from_command_line

sys.argv.insert(1, 'test')
execute_from_command_line(sys.argv)

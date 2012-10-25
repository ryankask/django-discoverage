#!/usr/bin/env python
import os.path
import re
from setuptools import setup, find_packages

def pkg_path(*components):
    path = os.path.join(os.path.dirname(__file__), *components)
    return os.path.realpath(path)

def get_readme():
    with open(pkg_path('README.rst'), 'r') as readme:
        return readme.read()

def get_version():
    with open(pkg_path('discoverage', '__init__.py'), 'r') as init:
        contents = init.read()
        match = re.search(r'__version__ = [\'"]([.\w]+)[\'"]', contents)
        return match.group(1)

setup(
    name='django-discoverage',
    version=get_version(),
    author='Ryan Kaskel',
    author_email='dev@ryankaskel.com',
    url='https://github.com/ryankask/django-discoverage',
    packages=find_packages(),
    install_requires=['coverage>=3.5.3', 'django-discover-runner>=0.2.2'],
    description='Jannis Leidel and Carl Meyer\'s django-discover-runner with coverage.',
    long_description=get_readme(),
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing',
    ]
)

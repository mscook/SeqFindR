#!/usr/bin/env python

# Note: Based on https://github.com/kennethreitz/requests/blob/master/setup.py
# See: http://docs.python.org/2/distutils/setupscript.html

import os
import sys

import SeqFindR

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'SeqFindR',
]

requires = []
with open('requirements.txt') as fin:
    lines = fin.readlines()
for l in lines:
    requires.append(l.strip())

setup(
    name='SeqFindR',
    version=SeqFindR.__version__,
    description='SeqFindR - easily create informative genomic feature plots',
    long_description=open('README.rst').read(),
    author='Mitchell Stanton-Cook',
    author_email='m.stantoncook@gmail.com',
    url='https://github.com/mscook/SeqFindR',
    packages=packages,
    scripts = ['SeqFindR/SeqFindR'],
    package_data={'': ['LICENSE']},
    package_dir={'SeqFindR': 'SeqFindR'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=False,
)

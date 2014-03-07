#!/usr/bin/env python

import os
import sys
import urllib
import SeqFindR.__init__ as meta
import setuptools

# Clean up
os.system("rm -rf build/ dist/ SeqFindR.egg-info/")

# Upload to PyPI
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

# Ensure that we have the latest pip version.
pip_support = 'http://pip.readthedocs.org/en/latest/installing.html'
print "We are going to install pip/upgrade it to the latest."
print "You may need root/admin to do this."
print "If it fails please see: %s" % (pip_support)
urllib.urlretrieve ("https://raw.github.com/pypa/pip/master/contrib/"
                        "get-pip.py", "get-pip.py")
os.system("python get-pip.py")
os.system("rm get-pip.py")
reload(setuptools)
from setuptools import setup

# Let install the requirements like this...
os.system("pip install -r requirements.txt")

packages = [
    meta.__title__,
]

requires = []
with open("requirements.txt") as fin:
    for line in fin:
        requires.append(line.strip())

setup(
    name                 = meta.__title__,
    version              = meta.__version__,
    description          = meta.__description__,
    long_description     = open('README.rst').read(),
    author               = meta.__author__,
    author_email         = meta.__author_email__,
    url                  = meta.__url__,
    packages             = packages,
    scripts              = [meta.__title__+'/'+meta.__title__, 
                            meta.__title__+'/vfdb_to_seqfindr'],
    package_data         = {'': ['LICENSE'], '': ['requirements.txt'],},
    package_dir          = {meta.__title__: meta.__title__},
    include_package_data = True,
    install_requires     = requires,
    license              = meta.__license__,
    zip_safe             = False,
    classifiers          =(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Visualization',
    ),
)

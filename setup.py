#!/usr/bin/env python

import os
import sys

import SeqFindR.__init__ as meta

try:                                                                                                                                                                    
    from setuptools import setup
except ImportError:
    # Bootstrap if we don't have setuptools available
    from ez_setup import use_setuptools
    use_setuptools()


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

os.system("pip install -r pre_requirements.txt")
os.system("pip install -r requirements.txt")

packages = [
    meta.__title__,
]

requires = ['numpy>=1.6.1',
            'scipy>=0.10.1',
            'matplotlib>=1.1.0',
            'biopython>=1.59',
            'ghalton>=0.6'
        ]

#with open('requirements.txt') as fin:
#    lines = fin.readlines()
#for l in lines:
#    requires.append(l.strip())

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

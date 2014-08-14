#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get version number
defs = {}
with open(path.join(here, 'src/archicow/defs.py')) as f:
    exec(f.read(), defs)

setup(
    name='archicow',
    version=defs['__version__'],
    description=defs['app_description'],
    long_description=long_description,
    #url='',
    author="Michal Belica",
    author_email="devel@beli.sk",
    license="GPL-3",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        # TODO 'Programming Language :: Python :: 3',
        'Topic :: System :: Archiving :: Backup',
        ],
    keywords=['backup'],
    zip_safe=True,
    install_requires=[
        'unipath',
        ],
    package_dir={'': 'src'},
    packages=['archicow', 'archicow.process', 'archicow.storage'],
    entry_points={
        'console_scripts': [
            'archicow = archicow:main',
            ],
        },
    )


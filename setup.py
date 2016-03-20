#!/usr/bin/env python

from distutils.core import setup

setup(
    name='fabee',
    version='0.1',
    author='Fabian Sinz',
    author_email='sinz@bcm.edu',
    description='Schemata for experiments by Fabian. ',
    # url='https://github.com/datajoint/datajoint-python',
    packages=['fabee'],
    requires=['numpy', 'pymysql', 'matplotlib','datajoint', 'commons'],
    license = "MIT",
)

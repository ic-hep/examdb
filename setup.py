#!/usr/bin/env python

import sys
from setuptools import setup, find_packages

REQUIRES = ['sqlalchemy']
REQUIRES2 = ['python-ldap']
REQURIES3 = ['pyldap']

if sys.version_info[0] < 3:
  REQUIRES.extend(REQUIRES2)
else:
  REQUIRES.extend(REQURIES3)


setup(name='examdb',
      version='1.0',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=REQUIRES,
     )


#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='examdb',
      version='1.0',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=['python-ldap', 'sqlalchemy'],
     )


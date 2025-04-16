#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages

_ = setup(
    name='tododav',
    version='0.0.3',
    author='Manuel Senfft',
    author_email='info@tagirijus.de',
    description='an abstraction layer for the caldav Python module',
    license='MIT',
    keywords='nextcloud tasks todo',
    packages=find_packages(),
    install_requires=[
        'caldav~=1.4.0'
    ],
)

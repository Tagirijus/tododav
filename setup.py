#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages

_ = setup(
    name='tododav',
    version='0.0.1',
    author='Manuel Senfft',
    author_email='info@tagirijus.de',
    description='A CalDAV VTODO abstraction layer module.',
    license='MIT',
    keywords='nextcloud tasks todo',
    packages=find_packages(),
    install_requires=[
        'caldav~=1.4.0'
    ],
)

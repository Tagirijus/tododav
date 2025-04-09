#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages

_ = setup(
    name='todomanager',
    version='0.0.0',
    author='Manuel Senfft',
    author_email='info@tagirijus.de',
    description='Simple program and website for managing NextCloud tasks',
    license='MIT',
    keywords='nextcloud tasks todo planner planning',
    packages=find_packages(),
    install_requires=[
        # 'click~=8.1',
        # 'rich~=13.7',
        # 'PyYaml~=6.0',
    ],
)

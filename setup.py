#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "travispls",
    version = "1.0.0",
    packages = find_packages('src'),
    package_dir = { '': 'src'},
    author = "Naftuli Kay",
    author_email = "me@naftuli.wtf",
    url = "https://github.com/naftulikay/travis-pls",
    install_requires = [
        'setuptools'
    ],
    dependency_links = [],
    entry_points = {
        'console_scripts': [
            'travis-pls = travispls:main'
        ]
    }
)

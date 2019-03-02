#!/usr/bin/env python3
"""
Copyright (C) 2018 Oto Kaláb
Contact: oto.kalab@opengeolabs.cz
"""

from setuptools import setup


with open("requirements.txt") as f:
    install_requirements = f.read().splitlines()

setup(name='nd_aopk',
        author='Oto Kaláb',
        author_email='oto.kalab@opengeolabs.cz',
        maintainer="Oto Kaláb",
        maintainer_email='oto.kalab@opengeolabs.cz',
        url='https://github.com/foo/bar/',
        description='',
        version="1.0.0",
        packages=[],
        long_description=open('README.md').read(),
        scripts=["nd_aopk.py"],

        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3'
            ],

        install_requires=install_requirements,
        keywords='GIS, AOPK, Nálezová databáze', 'Species occurences',
)

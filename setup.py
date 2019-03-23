#!/usr/bin/env python3
"""
Copyright (C) 2019 Oto Kaláb
Contact: oto.kalab@opengeolabs.cz
"""

from setuptools import setup


with open("requirements.txt") as f:
    install_requirements = f.read().splitlines()

setup(name='ndop-downloader',
        author='Oto Kaláb',
        author_email='oto.kalab@opengeolabs.cz',
        maintainer="Oto Kaláb",
        maintainer_email='oto.kalab@opengeolabs.cz',
        url='https://github.com/OpenGeoLabs/qgis-ndop-downloader',
        description='NDOP Downloader is an application for downloading of records of occurence from official database of the Nature Conservation Agency of the Czech Republic (Nálezová databáze Agentury ochrany přírody a krajiny ČR - NDOP - AOPK).',
        version="0.1.7",
        packages=["ndop"],
        long_description=open('README.rst').read(),
        scripts=["bin/ndop"],
        license="GNU/GPL3",
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Natural Language :: Czech',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3'
        ],

        install_requires=install_requirements,
        keywords=['GIS', 'AOPK', 'ecology', 'species occurences',
                  'NDOP', 'Czech Republic', 'nálezová databáze']
)

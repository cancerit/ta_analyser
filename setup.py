#!/usr/bin/env python3

from setuptools import setup

config = {
    'version': '1.0.0',
    'name': 'analyse_ta',
    'description': 'Tool to analyse TA repeats bed coverage...',
    'author': 'Shriram Bhosle',
    'url': 'https://github.com/cancerIT/analyse_ta',
    'author_email': 'cgphelp@sanger.ac.uk',
    'python_requires': '>= 3.6',
    'install_requires': ['tzlocal','pandas'],
    'packages': ['analyse_ta'],
    'package_data': {'analyse_ta':['data/*.bed.gz']},
    'entry_points': {
        'console_scripts': ['analyse_ta=analyse_ta.commandline:main'],
    }
}

setup(**config)


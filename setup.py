#!/usr/bin/python

import json

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Hector Rios',
    'url': 'https://github.com/hectron/affinity',
    'name': 'affinity',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['theme_converter']
}

with open('./config.json') as custom_settings:
    defaults = json.load(custom_settings)
    #config = { key: value for (key, value) in (config.items() + defaults.items()) }

setup(**config)
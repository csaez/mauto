from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

config = {
    'name': 'mauto',
    'description': 'mauto is a generic macro tool for Autodesk Maya.',
    'version': '0.1.0',
    'license': 'The MIT License',
    'author': 'Cesar Saez',
    'author_email': 'cesarte@gmail.com',
    'url': 'https://www.github.com/csaez/mauto',
    'packages': find_packages(exclude=['ez_setup', 'tests']),
    'package_data': {'mauto.gui': ['images/*.*']},
    'tests_require': ['nose', 'coverage', 'mock'],
    'scripts': []
}

setup(**config)

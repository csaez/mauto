from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

config = {
    'name': 'mauto',
    'description': 'mauto is a generic macro tool for Autodesk Maya.',
    'license': 'The MIT License',
    'packages': find_packages(exclude=['ez_setup', 'tests']),
    'package_data': {'mauto.gui': ['images/*.*']},
    'author': 'Cesar Saez',
    'author_email': 'cesarte@gmail.com',
    'url': 'https://www.github.com/csaez/mauto',
    'version': '0.1.0',
    'tests_require': ['nose'],
    'packages': ['mauto'],
    'scripts': []
}

setup(**config)

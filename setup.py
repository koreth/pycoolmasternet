#!/usr/bin/env python3
from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'pycoolmasternet',
    version = '0.0.2',
    license = 'MIT',
    description = 'Lightweight Python API for CoolMasterNet HVAC bridges',
    long_description = long_description,
    author = 'Steven Grimm',
    author_email = 'koreth@gmail.com',
    url = 'http://github.com/koreth/pycoolmasternet',
    packages = find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[],
    zip_safe=True,
    keywords='hvac homeautomation'
)

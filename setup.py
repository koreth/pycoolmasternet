#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name = 'pycoolmasternet',
    version = '0.0.1',
    license = 'MIT',
    description = 'Python library for CoolMasterNet bridges',
    author = 'Steven Grimm',
    author_email = 'koreth@gmail.com',
    url = 'http://github.com/koreth/pycoolmasternet',
    packages=find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[],
    zip_safe=True,
)

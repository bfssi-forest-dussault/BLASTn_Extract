#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="BLASTn_Extract",
    version="0.1",  # version must be incremented manually each time
    packages=find_packages(),
    author="Forest Dussault",
    author_email="forest.dussault@inspection.gc.ca",
    url="https://github.com/bfssi-forest-dussault/BLASTn_Extract",  # link to the repo
    scripts=['blastn_extract.py'],
    install_requires=['click']  # list all dependencies here
)
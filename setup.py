#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="AutoInterOp",
    version="0.1.2", # version must be incremented manually each time
    packages=find_packages(),
    author="Forest Dussault",
    author_email="forest.dussault@inspection.gc.ca",
    url="https://github.com/forestdussault/AutoInterOp",  # link to the repo
    scripts=['AutoInterOp.py'],
    install_requires=['click']  # list all dependencies here
)
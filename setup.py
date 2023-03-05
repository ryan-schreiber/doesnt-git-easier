#!/usr/bin/env python

from setuptools import setup, find_packages

with open("./requirements.txt") as f:
    requirements = f.read().split("\n")

setup(
      name='doesnt-git-easier',
      version='1.0.0',
      description='A library of common python utilities that can be generally used in python projects',
      author='Ryan Schreiber',
      author_email='ryanschreiber86@gmail.com',
      packages=find_packages(),
      install_requires=requirements
    )

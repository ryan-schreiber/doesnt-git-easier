#!/usr/bin/env python

from setuptools import setup, find_packages

with open("./requirements.txt") as f:
    requirements = f.read().split("\n")

with open("./version.txt") as f:
    version = f.read()

setup(
      name='doesnt-git-easier',
      version=version,
      description='Making it easy to read and write files to Git in a Pythonic way with context managers and the Git REST API.',
      long_description='Making it easy to read and write files to Git in a Pythonic way with context managers and the Git REST API.',
      author='Ryan Schreiber',
      author_email='ryanschreiber86@gmail.com',
      packages=find_packages(),
      install_requires=requirements,
      keywords="git commit add push files context manager doesnt-git-easier doesn't get easier",
      project_urls={
        'Documentation': 'https://github.com/ryan-schreiber/doesnt-git-easier/',
        'Source': 'https://github.com/ryan-schreiber/doesnt-git-easier/',
        'Tracker': 'https://github.com/ryan-schreiber/doesnt-git-easier/issues',
      },
    )

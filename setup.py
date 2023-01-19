#!/usr/bin/env python3
"""Setup the Traiter environment."""
from distutils.core import setup
from setuptools import find_packages

NAME = "traiterplants"
DESCRIPTION = """Common Traiter patterns for mining literature on plants"""


def readme():
    """Get README.md content."""
    with open("README.md") as in_file:
        return in_file.read()


def license_():
    """Get LICENSE.txt content."""
    with open("LICENSE") as in_file:
        return in_file.read()


def find_requirements():
    """Read requirements.txt file and returns list of requirements."""
    with open("requirements.txt") as in_file:
        return in_file.read().splitlines()


setup(
    name=NAME,
    version="0.1.0",
    packages=find_packages(),
    install_requires=find_requirements(),
    include_package_data=True,
    description=DESCRIPTION,
    long_description=readme(),
    license=license_(),
    url="https://github.com/rafelafrance/traiterplants",
    python_requires=">=3.10",
    scripts=[],
)

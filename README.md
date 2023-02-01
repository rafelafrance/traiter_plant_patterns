# traiter_plants ![Python application](https://github.com/rafelafrance/traiter_plants/workflows/CI/badge.svg)
Extract traits about plants from authoritative literature.

This repository contains rule-based parsers common to various plant parsing projects like:
- [traiter_efloras](https://github.com/rafelafrance/traiter_efloras)
- [traiter_mimosa](https://github.com/rafelafrance/traiter_mimosa)

## Install
You will need to have Python3.11+ installed, as well as pip, a package manager for Python.
Python 3.11+ is required because I'm using the new `tomllib` to read the `pyproject.toml` file in `setup.py`.
You can install the requirements into your python environment like so:
```bash
git clone https://github.com/rafelafrance/traiter_plants.git
cd traiter_plants
make install
```

## Repository details

## Run
This repository is a library for other Traiter projects and is not run directly.

## Tests
You can run the tests like so:
```bash
cd /my/path/to/traiter_plants
python -m unittest discover
```

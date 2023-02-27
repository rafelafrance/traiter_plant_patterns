.PHONY: test install dev venv clean
.ONESHELL:

VENV=.venv
PYTHON=./$(VENV)/bin/python3.11
PIP_INSTALL=$(PYTHON) -m pip install
SPACY_MODEL=$(PYTHON) -m spacy download en_core_web_sm
TERM_DB=./plants/pylib/vocabulary/plant_terms.sqlite
CREATE_DB=$(PYTHON) ./plants/create_dbs.py

test:
	$(PYTHON) -m unittest discover

install: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) .
	$(PIP_INSTALL) git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
	$(SPACY_MODEL)
	$(CREATE_DB)

dev: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) -e .[dev]
	$(PIP_INSTALL) -e ../traiter
	$(SPACY_MODEL)
	pre-commit install
	$(CREATE_DB)

venv:
	test -d $(VENV) || python3.11 -m venv $(VENV)

clean:
	rm -r $(VENV)
	rm -f $(TERM_DB)
	find -iname "*.pyc" -delete

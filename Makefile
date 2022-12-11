.ONESHELL:

.PHONY: dependencies, venv, run

dependencies:
	pip install -r requirements.txt

venv:
	source venv/bin/activate
	pip install -r requirements.txt

run:
	make venv
	python main.py


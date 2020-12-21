
CV_PKGS=castervoice test

all: lint test

lint:
	flake8 $(CV_PKGS)
	pylint --rcfile=setup.cfg $(CV_PKGS)

test:
	python -m unittest discover -p '*.py' -s test.castervoice.core

.PHONY: lint test

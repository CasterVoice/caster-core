
CV_PKGS=castervoice

all: lint test

lint:
	flake8 $(CV_PKGS)
	pylint --rcfile=setup.cfg $(CV_PKGS)

test:
	python -m unittest discover -p '*.py' -s castervoice.core

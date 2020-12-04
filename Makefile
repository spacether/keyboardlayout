.PHONY: test docs

develop:
	pip3 install -e .[dev]

install:
	pip3 install .

uninstall:
	pip3 uninstall keyboardlayout

test:
	python setup.py pytest

docs:
	rm -rf docs
	sphinx-build -b html sphinx docs
	touch docs/.nojekyll

.PHONY: test  dist docs

develop:
	pip3 install -e .[dev]

install:
	pip3 install .

uninstall:
	pip3 uninstall keyboardlayout

test:
	python3 setup.py pytest

docs:
	rm -rf docs
	sphinx-build -b html sphinx docs
	touch docs/.nojekyll

dist:
	python3 setup.py sdist bdist_wheel
	rm -rf build

testpypi:
	@read -p "Publish to testpypi? " -n 1 -r; \
	if [[ $$REPLY =~ ^[Nn] ]]; \
	then \
			echo "\nNot publishing"; exit 1; \
	fi
	make docs dist
	python -m twine upload --repository testpypi dist/*

pypi:
	@read -p "Publish to pypi? " -n 1 -r; \
	if [[ $$REPLY =~ ^[Nn] ]]; \
	then \
			echo "\nNot publishing"; exit 1; \
	fi
	make docs dist
	twine upload dist/*

VENV_PY  = python3
PYTHON   = python
PIP      = $(PYTHON) -m pip

.PHONY: build venv req buildreq test

build: req
	$(PYTHON) python/setup.py sdist bdist_wheel

req:
	$(PIP) install -r python/requirements.txt

test:
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	python -m pip install --index-url https://test.pypi.org/simple/ webcui

clean:
	rm -rf build

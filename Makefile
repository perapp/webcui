VENV_PY  = python3
PYTHON   = build/pyvenv/bin/python
PIP      = $(PYTHON) -m pip

.PHONY:
	build
	pyvenv
	test
	test_twine_env

build: pyvenv
	$(PYTHON) python/setup.py sdist --dist-dir build/dist
	$(PYTHON) python/setup.py bdist_wheel --dist-dir build/dist
pyvenv: build/pyvenv
build/pyvenv:
	$(VENV_PY) -m venv build/pyvenv
	$(PIP) install --upgrade setuptools wheel twine
	$(PIP) install -r python/requirements.txt

test: test_twine_env
	$(PYTHON) -m twine upload -u ${PYPI_USER} -p ${PYPI_PASSWORD} --repository-url https://test.pypi.org/legacy/ build/dist/*
	echo $(PYTHON) -m pip install --index-url https://test.pypi.org/simple/ webcui

deploy:
	$(PYTHON) -m twine upload -u "$PYPI_USER" -p "$PYPI_PASSWORD" build/dist/*

clean:
	rm -rf build
	rm -rf python/webcui.egg-info

test_twine_env:
ifeq (${PYPI_USER},)
	echo "PYPI_USER variable not set" >&2
	exit 1
endif
ifeq (${PYPI_PASSWORD},)
	echo "PYPI_PASSWORD variable not set" >&2
	exit 1
endif


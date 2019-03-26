VENV_PY  = python3
PYTHON   = build/buildenv/bin/python
TPYTHON  = build/testenv/bin/python

.PHONY:
	build
	test
	test_twine_env

build: build/buildenv
	$(PYTHON) python/setup.py sdist --dist-dir build/dist
	$(PYTHON) python/setup.py bdist_wheel --dist-dir build/dist

test: build/testenv
	PYTHONPATH=python $</bin/python -m pytest test

run: build/testenv
	PYTHONPATH=python $</bin/python test/app/test_basic_app.py

test_deploy: test_twine_env
	$(PYTHON) -m twine upload -u ${PYPI_USER} -p ${PYPI_PASSWORD} --repository-url https://test.pypi.org/legacy/ build/dist/*
	$(VENV_PY) -m venv build/testenv
	$(TPYTHON) -m pip install --index-url https://test.pypi.org/simple/ webcui
	$(TPYTHON) -m pytest test

deploy:
	$(PYTHON) -m twine upload -u "$PYPI_USER" -p "$PYPI_PASSWORD" build/dist/*

build/buildenv:
	$(VENV_PY) -m venv $@
	$@/bin/python -m pip install --upgrade setuptools wheel twine
build/testenv:
	$(VENV_PY) -m venv $@
	$@/bin/python -m pip install pytest -r python/requirements.txt
build/testpypienv:
	$(VENV_PY) -m venv $@
	$@/bin/python -m pip install pytest
	$@/bin/python -m pip install --index-url https://test.pypi.org/simple/ webcui
build/pypienv:
	$(VENV_PY) -m venv $@
	$@/bin/python -m pip install pytest webcui

clean:
	rm -rf build
	rm -rf python/*.egg-info

test_twine_env:
ifeq (${PYPI_USER},)
	echo "PYPI_USER variable not set" >&2
	exit 1
endif
ifeq (${PYPI_PASSWORD},)
	echo "PYPI_PASSWORD variable not set" >&2
	exit 1
endif


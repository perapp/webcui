ifeq (${OS},Windows_NT)
	PYTHON_SYS = python.exe
	PYTHON     = Scripts/python.exe
else
	PYTHON_SYS = python3
	PYTHON     = bin/python
endif

.PHONY:
	build
	test
	test_twine_env

build: build/env/build
	$</$(PYTHON) python/setup.py sdist --dist-dir build/dist
	$</$(PYTHON) python/setup.py bdist_wheel --dist-dir build/dist

test: build/env/test
	$</$(PYTHON) -m pytest test

run: build/testenv
	PYTHONPATH=python $</bin/python test/app/test_basic_app.py

test_deploy: test_twine_env
	$(PYTHON) -m twine upload -u ${PYPI_USER} -p ${PYPI_PASSWORD} --repository-url https://test.pypi.org/legacy/ build/dist/*
	$(VENV_PY) -m venv build/testenv
	$(TPYTHON) -m pip install --index-url https://test.pypi.org/simple/ webcui
	$(TPYTHON) -m pytest test

deploy:
	$(PYTHON) -m twine upload -u "$PYPI_USER" -p "$PYPI_PASSWORD" build/dist/*

build/env/build:
	$(PYTHON_SYS) python/buildtools/buildenv.py $(@F)
build/env/test:
	$(PYTHON_SYS) python/buildtools/buildenv.py $(@F)
build/env/testpypi:
	$(VENV_PY) -m venv $@
	$@/bin/python -m pip install pytest
	$@/bin/python -m pip install --index-url https://test.pypi.org/simple/ webcui
build/env/pypi:
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


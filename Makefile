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

build: build/env/build
	$</$(PYTHON) python/setup.py sdist --dist-dir build/dist
	$</$(PYTHON) python/setup.py bdist_wheel --dist-dir build/dist

test: build/env/test
	$</$(PYTHON) -m pytest test

run: build/testenv
	$</$(PYTHON) test/app/test_basic_app.py

test_deploy: build/env/testpypi build
	$</$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ build/dist/*
	$</$(PYTHON) -m pip install --index-url https://test.pypi.org/simple/ webcui
	$</$(PYTHON) -m pytest test

deploy: build/env/build build
	$</$(PYTHON) -m twine upload build/dist/*

build/env/build:
	$(PYTHON_SYS) python/buildtools/buildenv.py $(@F)
build/env/test:
	$(PYTHON_SYS) python/buildtools/buildenv.py $(@F)
build/env/testpypi:
	$(PYTHON_SYS) python/buildtools/buildenv.py $(@F)
build/env/pypi:
	$(PYTHON_SYS) python/buildtools/buildenv.py $(@F)

clean:
	rm -rf build
	rm -rf python/*.egg-info

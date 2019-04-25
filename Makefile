ifeq (${OS},Windows_NT)
	PYTHON_SYS = python.exe
	PYTHON     = Scripts/python.exe
else
	PYTHON_SYS = python3
	PYTHON     = bin/python
endif

.PHONY:	build docker test

build: foo build/env/build docker
	$</$(PYTHON) python/setup.py sdist --dist-dir build/dist
	$</$(PYTHON) python/setup.py bdist_wheel --dist-dir build/dist

foo:
	ls -l /var/run/

docker: build/docker/debian.log build/docker/deployenv.log

build/docker/debian.log: docker/debian.docker
	mkdir -p build/docker
	docker build -t perapp/webcui_debian -f docker/debian.docker . && touch $@

build/docker/deployenv.log: build/docker/debian.log docker/deployenv.docker
	mkdir -p build/docker
	docker build -t perapp/webcui_deployenv -f docker/deployenv.docker . && touch $@

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
	docker images -q perapp/webcui_deployenv | xargs -r docker rmi
	docker images -q perapp/webcui_debian | xargs -r docker rmi

ifeq (${OS},Windows_NT)
	PYTHON_SYS := python.exe
	PYTHON     := Scripts/python.exe
else
	PYTHON_SYS := python3
	PYTHON     := bin/python
endif
ifeq (${VERSION},)
	export VERSION = $(shell date --utc -Iseconds | sed 's/://g; s/+.*//')
endif
ifeq (${DOCKER_PREFIX},)
	export DOCKER_PREFIX := local/webcui/
endif

PYTHON  := poetry run python

.PHONY:	build docker test

build:
	poetry build

docker: docker/debian.dockerimage docker/deployenv.dockerimage docker/webcui.dockerimage

%.dockerimage: %.docker
	$(eval IMG=$(DOCKER_PREFIX)$(*F))
	docker pull $(IMG):latest || true
	docker build -t $(IMG):latest -t $(IMG):$(VERSION) -f $< .
	#docker push $(IMG):$(VERSION) || true
	#docker push $(IMG):latest || true

docker: $(obj)

devenv:
	$(PYTHON_SYS) -m pip install --user pipx
	pipx install poetry
	poetry install

test:
	poetry run python -m pytest -s --tb=native test

publish: build
	poetry publish

shell:
	poetry shell

clean:
	rm -rf dist
	find . -name webcui.egg-info | xargs rm -rf
	find . -name __pycache__ | xargs rm -rf
	docker ps -f label=org.pypi.webcui -qa | xargs -r docker kill
	docker ps -f label=org.pypi.webcui -qa | xargs -r docker rm

xclean: clean
	docker images -qa $(DOCKER_PREFIX)\* | xargs -r docker rmi -f

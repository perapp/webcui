ifeq (${OS},Windows_NT)
	PYTHON_SYS = python.exe
	PYTHON     = Scripts/python.exe
else
	PYTHON_SYS = python3
	PYTHON     = bin/python
endif
PYTHON = poetry run python

.PHONY:	build docker test

devenv:
	$(PYTHON_SYS) -m pip install --user pipx
	pipx install poetry
	poetry install

build:
	poetry build

test:
	poetry run python test/mkdocker.py
	poetry run python -m pytest test

publish: build
	poetry publish

shell:
	poetry shell

clean:
	$(PYTHON) buildtools/clean.py --all

xclean: clean
	$(PYTHON) buildtools/clean.py --all

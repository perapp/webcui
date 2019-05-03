FROM python:latest

RUN pip install poetry
RUN mkdir /project
WORKDIR /project

ADD pyproject.toml poetry.lock /project/
RUN poetry install

ADD . /project
CMD poetry run python

FROM python:3.10

ADD . /app

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install
FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev \
    && apt-get install -y libpq-dev \
    && pip install psycopg2 \
    && apt-get clean

COPY . /code/
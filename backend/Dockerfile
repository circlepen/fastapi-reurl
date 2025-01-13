FROM amd64/python:3.8-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get clean \
    && pip install psycopg2


RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/
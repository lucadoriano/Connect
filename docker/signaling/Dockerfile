FROM python:3.12-alpine

RUN apk update && apk upgrade --no-cache

COPY ./python_packages /usr/local/lib/python3.12/site-packages

WORKDIR /usr/local/lib/python3.12/site-packages/src/
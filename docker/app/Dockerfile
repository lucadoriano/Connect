FROM python:3.12-alpine

RUN apk update && apk upgrade --no-cache

RUN apk add --no-cache \
    bash python3-dev build-base linux-headers pcre-dev

COPY  ./requirements.txt /

RUN pip install -r requirements.txt

RUN rm -r ./requirements.txt

COPY ./python_packages /usr/local/lib/python3.12/site-packages

WORKDIR /usr/local/lib/python3.12/site-packages/src/
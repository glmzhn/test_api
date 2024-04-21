FROM python:3.12-alpine3.19

COPY requirements.txt /temp/requirements.txt
COPY test_api /test_api
WORKDIR test_api
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user
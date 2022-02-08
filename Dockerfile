FROM python:3.9-slim

RUN apt-get update \
    && apt-get install --yes --no-install-recommends git-core \
    && rm --recursive --force /var/lib/apt/lists/* \
    && pip3 install --upgrade pip \
    && pip3 install django==4.0

COPY . /opt/jumpstart/

WORKDIR /do/not/work/here
ENTRYPOINT ["/bin/sh", "/opt/jumpstart/start.sh"]

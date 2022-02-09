FROM python:3.9-slim

COPY requirements.txt /opt/jumpstart/requirements.txt
RUN apt-get update \
    && apt-get install --yes --no-install-recommends git-core \
    && rm --recursive --force /var/lib/apt/lists/* \
    && pip3 install --upgrade pip \
    && pip3 install -r /opt/jumpstart/requirements.txt

COPY . /opt/jumpstart/

WORKDIR /do/not/work/here
ENTRYPOINT ["/bin/sh", "/opt/jumpstart/start.sh"]

FROM python:3.6

ENV JUMPSTART_PRINT_SCRIPT=yes

RUN apt-get update \
    && apt-get install --yes --no-install-recommends git-core \
    && rm --recursive --force /var/lib/apt/lists/* \
    && pip3 install django==2.1

COPY . /opt/jumpstart/

ENTRYPOINT ["/bin/sh", "/opt/jumpstart/start.sh"]

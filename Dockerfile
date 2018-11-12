FROM python:3.6-alpine

RUN pip3 install django==2.1

COPY . /opt/jumpstart/

ENTRYPOINT ["/usr/local/bin/python3", "/opt/jumpstart/jumpstart.py"]

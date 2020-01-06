FROM python:2-stretch

MAINTAINER Mahyuddin Susanto <udienz@gmail.com>

RUN apt update && \
    apt dist-upgrade -y -q && \
    apt install -y python-libxslt1 python-libxml2 python-genshi xsltproc \
    python-django git python-lxml vim python-librdf

RUN git clone https://github.com/rubys/venus 
WORKDIR /home/venus

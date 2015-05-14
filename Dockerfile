# Dockerfile for PRISONER
# http://prisoner.cs.st-andrews.ac.uk

# Version 0.1
# Last updated May 7th 2015


FROM ubuntu
MAINTAINER Luke Hutton <lh49@st-andrews.ac.uk>

LABEL Description="This image prepares a virtual environment with the dependencies needed to execute a PRISONER instance"

# creates a virtual environment for PRISONER
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y python python-dev python-distribute python-pip libxml2-dev libxslt1-dev zlib1g-dev

COPY ./ /usr/bin/prisoner/

# install python requirements into this environment
RUN pip install -r /usr/bin/prisoner/requirements.txt

EXPOSE 5000

CMD ["python","/usr/bin/prisoner/server/prisoner.wsgi"]
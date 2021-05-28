FROM ubuntu:20.04 as baseimage
LABEL maintainer="desh"

RUN  apt-get update && apt-get install -y lsb-release && apt-get clean all
RUN  apt-get install -y gnupg2 wget

RUN  apt-get update

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get install -y software-properties-common
RUN apt-add-repository universe
#RUN add-apt-repository ppa:fkrull/deadsnakes

RUN apt-get update && apt-get install --no-install-recommends -y \
    software-properties-common \
    build-essential \
    curl \
    git \
    locales \
    libffi-dev \
    libssl-dev \
    sudo \
    vim \
    wget \
    dos2unix \
    less
#     python3-pip

#RUN apt-get install -y postgresql-12

RUN apt-get clean all

# RUN apt-get install -y nodejs npm
# ENV PATH /usr/local/bin/:$PATH
# RUN npm install -g @angular/cli@9

# RUN ln -s /usr/bin/python3 /usr/bin/python
# RUN ln -s /usr/bin/pip3 /usr/bin/pip

# docker build -t baseimage:latest .

#######################################
#  django build
#######################################

FROM baseimage
LABEL maintainer="desh"

# let's install minimum packages required
# for installation of postgres
RUN locale-gen en_AU.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -


RUN apt-get update
RUN apt-get clean all
# install postgres server and client, we are installing version 12
RUN apt-get install -y postgresql-client-13

# set work directory
WORKDIR /addr/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    python3-pip

RUN ln -s /usr/bin/python3 /usr/bin/python
#RUN ln -s /usr/bin/pip3 /usr/bin/pip

# RUN adduser --disabled-password --gecos '' addr
# RUN usermod -aG sudo addr

# install dependencies
RUN pip3 install --upgrade pip
#RUN pip install -r ./django/requirements.txt
COPY ./django/requirements.txt .

RUN apt-get update
RUN apt-get install -y libpq-dev python3-dev cron rsyslog
RUN touch /var/log/cron.log

RUN pip3 install -r requirements.txt

ARG PG_USER
ARG PG_PASSWORD
ARG PG_DATABASE

ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DATABASE

ARG PROJ_ROOT
ARG PROJ_OPS
ARG PYTHONPATH

ENV PG_USER=${POSTGRES_USER}
ENV PG_PASSWORD=${POSTGRES_PASSWORD}
ENV PG_DATABASE=${POSTGRES_DB}
ENV PROJ_ROOT=${PROJ_ROOT}
ENV PROJ_OPS=$PROJ_OPS

VOLUME  ["/addr/"]
WORKDIR /addr/
# USER addr

COPY ./django/bashrc.text /etc/environment
RUN chmod +x /etc/environment
RUN dos2unix /etc/environment
COPY ./django/entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh

CMD ["sh", "/entrypoint.sh"]

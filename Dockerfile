# We're using Alpine stable
FROM alpine:3.9

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' -i /etc/apk/repositories

# Installing Python 
RUN apk add --no-cache --update \
    git \
    bash \
    libffi-dev \
    openssl-dev \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    sqlite-dev \
    build-base

# Set Python version
ARG PYTHON_VERSION='3.8-dev'
# Set pyenv home
ARG PYENV_HOME=/root/.pyenv
# Note installing THROUGH THIS METHOD WILL DELAY DEPLOYING
# Install pyenv, then install python versions
RUN git clone --depth 1 https://github.com/pyenv/pyenv.git $PYENV_HOME && \
    rm -rfv $PYENV_HOME/.git

ENV PATH $PYENV_HOME/shims:$PYENV_HOME/bin:$PATH

RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION
RUN pip install --upgrade pip && pyenv rehash
# Cleaning pip cache
RUN rm -rf ~/.cache/pip
#
# Install all the required packages
#
RUN apk add --no-cache \
    py-pillow py-requests py-sqlalchemy py-psycopg2 git py-lxml \
    libxslt-dev py-pip libxml2 libxml2-dev libpq postgresql-dev \
    postgresql build-base linux-headers jpeg-dev \
    curl neofetch git sudo gcc python-dev python3-dev \
    postgresql postgresql-client php-pgsql libwebp-dev libwebp-tools \
    musl postgresql-dev
RUN apk add --no-cache sqlite
RUN apk add figlet 
# Installing Telethon externally
RUN git clone https://www.github.com/LonamiWebs/Telethon Telethon \
&& cd Telethon \
&& python setup.py install 

# Copy Python Requirements to /app
RUN git clone https://www.github.com/psycopg/psycopg2 psycopg2 \
&& cd psycopg2 \
&& python setup.py install
# Cloning Userbot Files to directory /home/
RUN mkdir /home/Telegram-UserBot
RUN git clone https://github.com/Thagoo/Tbot2 -b staging /home/Telegram-UserBot
WORKDIR /home/Telegram-UserBot
# Making sudo
RUN  sed -e 's;^# \(%wheel.*NOPASSWD.*\);\1;g' -i /etc/sudoers
RUN adduser userbot --disabled-password --home /home/userbot
RUN adduser userbot wheel
USER userbot

#
# Install requirements
#
RUN sudo pip3 install -r requirementsDock.txt
# Removal PIP package caching
RUN rm -rf ~/.cache/pip
#
# Running userbot
#
CMD ["python3","-m","userbot"]

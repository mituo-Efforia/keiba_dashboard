FROM python:3.10.12
USER root

RUN apt_get update
RUN apt_get -y install locales
RUN apt_get install -y vim less
RUN apt_get install -y zsh less


RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

#dash
RUN pip install
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD . /flask-scrapy
WORKDIR /flask-scrapy
RUN pip install -r requirements.txt

COPY . /flask-scrapy/

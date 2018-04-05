FROM python:3.6-alpine
MAINTAINER Dmitry Bubnenkov
RUN python -m pip install --upgrade pip
RUN apk update \
    && apk add libpq postgresql-dev \
    && apk add build-base \
    && apk add python-dev \
    && apk add libc-dev \
    && apk add linux-headers 
RUN pip install psycopg2
RUN pip install psycopg2-binary
EXPOSE 9000
WORKDIR /app/tr_extractor
COPY . /app/tr_extractor
RUN pip install -r requirements.txt
CMD ["uwsgi", "--ini", "/app/tr_extractor/config.ini"]

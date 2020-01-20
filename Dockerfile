FROM python:3.6-slim-buster as BASE
WORKDIR /usr/src/app
ADD . .
RUN apt-get update -qq
RUN apt-get install -yqq make
RUN apt-get install -yqq curl
RUN apt-get install -yqq --no-install-recommends vim

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

ENTRYPOINT ["make", "activate"]
FROM python:3.7
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN pip install pipenv
RUN pipenv install --system --deploy

ARG TEST
ENV DOCKERIZE_VERSION v0.6.1
RUN [ "x$TEST" = "x" ] && true || pipenv install --system --deploy --dev
RUN [ "x$TEST" = "x" ] && true || curl -L -s -o dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz
RUN [ "x$TEST" = "x" ] && true || tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz
RUN [ "x$TEST" = "x" ] && true || rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY . /code/
RUN ["chmod", "+x", "test/test.sh"]

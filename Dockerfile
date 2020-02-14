FROM python:3.7
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN pip install pipenv
RUN pipenv install --system --deploy --dev
COPY . /code/

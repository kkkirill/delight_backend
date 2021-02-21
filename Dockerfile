ARG PYSETUP_PATH="/opt/pysetup"

FROM python:3.8-slim as base
ARG PYSETUP_PATH
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=100 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH=$PYSETUP_PATH \
    VENV_PATH="/opt/pysetup/.venv"

FROM base as builder
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential
#RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --version $POETRY_VERSION
RUN pip install poetry==$POETRY_VERSION
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt -o $PYSETUP_PATH/requirements.txt --without-hashes


FROM python:3.8-slim as app
ARG PYSETUP_PATH
ARG TEST
ENV IS_TEST=$TEST
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
RUN pip install --no-cache-dir -r $PYSETUP_PATH/requirements.txt
WORKDIR /app
COPY . /app/


RUN ["chmod", "+x", "entrypoint.sh"]
ENTRYPOINT ["entrypoint.sh", "$IS_TEST"]

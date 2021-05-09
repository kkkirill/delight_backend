#!/usr/bin/env bash

TRY_LOOP="15"
WAIT_SECONDS=5

: "${POSTGRES_HOST:="db"}"
: "${POSTGRES_PORT:="5432"}"
: "${LOCALSTACK_HOST:="localstack"}"
: "${LOCALSTACK_PORT:="4566"}"
: "${REDIS_HOST:="redis"}"
: "${REDIS_PORT:="6379"}"

wait_for_port() {
  local name="$1" host="$2" port="$3"
  local j=0
  while ! nc -z "$host" "$port" >/dev/null 2>&1 < /dev/null; do
    j=$((j+1))
    if [ $j -ge $TRY_LOOP ]; then
      echo >&2 "$(date) - $host:$port still not reachable, giving up"
      exit 1
    fi
    echo "$(date) - waiting for $name... $j/$TRY_LOOP"
    sleep $WAIT_SECONDS
  done
}

if [ -n "${IS_TEST}" ]; then
  wait_for_port "Localstack" "$LOCALSTACK_HOST" "$LOCALSTACK_PORT"
  wait_for_port "Postgres" "$POSTGRES_HOST" "$POSTGRES_PORT"
  wait_for_port "Redis" "$REDIS_HOST" "$REDIS_PORT"

  localstack_http_endpoint="http://$LOCALSTACK_HOST:$LOCALSTACK_PORT/health?reload"
  iterations=0
  while true
  do
    ((iterations++))
    sleep $WAIT_SECONDS

    http_code=$(curl -s -I -L -o /dev/null -w '%{http_code}' "$localstack_http_endpoint";)
    echo "Attempt $iterations, Localstack Status code: $http_code"

    if [ "$http_code" -eq 200 ]; then
      break
    fi

    if [ $iterations -ge $TRY_LOOP ]; then
      echo "Localstack startup timeout"
      exit 1
    fi
  done

  echo "waiting for 10s ..."
  sleep 10
fi

exec "$@"
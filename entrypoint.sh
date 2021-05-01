#!/usr/bin/env bash

TRY_LOOP="15"

: "${POSTGRES_HOST:="db"}"
: "${POSTGRES_PORT:="5432"}"
: "${LOCALSTACK_HOST:="localstack"}"
: "${LOCALSTACK_PORT:="4571"}"
: "${REDIS_HOST:="redis"}"
: "${REDIS_PORT:="6379"}"

wait_for_port() {
  local name="$1" host="$2" port="$3"
  echo $name $host $port
  local j=0
  nc -z "$host" "$port"
  while ! nc -z "$host" "$port" >/dev/null 2>&1 < /dev/null; do
    j=$((j+1))
    if [ $j -ge $TRY_LOOP ]; then
      echo >&2 "$(date) - $host:$port still not reachable, giving up"
      exit 1
    fi
    echo "$(date) - waiting for $name... $j/$TRY_LOOP"
    sleep 5
  done
}

if [ -n "${IS_TEST}" ]; then
  wait_for_port "Postgres" "$POSTGRES_HOST" "$POSTGRES_PORT"
  wait_for_port "Redis" "$REDIS_HOST" "$REDIS_PORT"
  wait_for_port "Localstack" "$LOCALSTACK_HOST" "$LOCALSTACK_PORT"
fi

exec "$@"
APP_NAME := delight
APP_HASH := $(shell git rev-parse --short HEAD)

export APP_NAME
export APP_HASH

build_test:
	@docker-compose \
		-f docker-compose.yaml \
		-f docker-compose.test.yaml \
		build --parallel web

.PHONY: test
test: build_test
	@docker-compose \
		-f docker-compose.yaml \
		-f docker-compose.test.yaml \
		run web

run:
	@docker-compose up

run_rebuild:
	@docker-compose build --parallel

exec:
	@docker-compose -f docker-compose.yaml exec web $(cmd)

migrate: cmd=python manage.py migrate
migrate: exec

fake_data: cmd=python manage.py fake_data
fake_data: exec

clear_all:
	@docker-compose \
		-f docker-compose.yaml \
		-f docker-compose.test.yaml \
		down -v

fix:
	poetry run black .
	poetry run pylama
	poetry run isort --recursive .

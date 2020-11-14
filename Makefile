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
		run web dockerize -timeout 20s -wait tcp://db:5432 bash -c "test/test.sh"

run:
	@docker-compose up

run+rebuild:
	@docker-compose up --build

clear_all:
	@docker-compose \
		-f docker-compose.yaml \
		-f docker-compose.test.yaml \
		down -v

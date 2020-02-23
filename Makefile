APP_NAME := vibrer
APP_HASH := $(shell git rev-parse --short HEAD)

export APP_NAME
export APP_HASH

build_test:
	@docker-compose \
		-f docker-compose.yaml \
		-f docker-compose.test.yaml \
		build web

.PHONY: test
test: build_test
	@docker-compose \
		-f docker-compose.yaml \
		-f docker-compose.test.yaml \
		run web dockerize -timeout 20s -wait tcp://db:5432 bash -c "test/test.sh"
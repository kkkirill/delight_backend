build:
	@docker-compose build --parallel web

build_test:
	@docker-compose \
		-f docker-compose.yaml \
		-f docker-compose.test.yaml \
		build --parallel web

clear_all:
	@docker-compose \
		-f docker-compose.yaml \
		-f docker-compose.test.yaml \
		down -v

run:
	@docker-compose up

exec:
	@docker-compose -f docker-compose.yaml exec web $(cmd)

test: build_test
	@docker-compose \
		-f docker-compose.yaml \
		-f docker-compose.test.yaml \
		run web

migrate: cmd=python manage.py migrate
migrate: exec

fake_data: cmd=python manage.py fake_data
fake_data: exec

fix:
	poetry run black .
	poetry run pylama
	poetry run isort --recursive .

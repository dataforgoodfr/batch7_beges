build:
	docker-compose build

run-bash:
	docker-compose -f docker-compose.yml -f docker-compose-dev.yml run --rm --service-ports beges /bin/bash

run-prod-server:
	docker-compose -f docker-compose.yml -f docker-compose-prod.yml up

run-dev-server:
	docker-compose -f docker-compose.yml -f docker-compose-dev.yml up

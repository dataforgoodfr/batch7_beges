build:
	docker-compose build

download-datasets:
	docker-compose -f docker-compose.yml -f docker-compose-dev.yml run --rm beges sh scripts/download_datasets.sh

prepare-datasets:
	docker-compose -f docker-compose.yml -f docker-compose-dev.yml run --rm beges python scripts/prepare_datasets.py

down:
	docker-compose down

run-bash:
	docker-compose -f docker-compose.yml -f docker-compose-dev.yml run --rm --service-ports beges /bin/bash

run-prod-server:
	docker-compose -f docker-compose.yml -f docker-compose-prod.yml up -d

run-dev-server:
	docker-compose -f docker-compose.yml -f docker-compose-dev.yml up

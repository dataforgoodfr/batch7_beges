build:
	docker-compose build

download-datasets:
	git lfs pull
	unzip -o ./data/raw/chorus-dt/first_semester.zip -d ./data/raw/chorus-dt
	unzip -o ./data/raw/chorus-dt/second_semester.zip -d ./data/raw/chorus-dt

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

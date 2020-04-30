# Installation

## Requirements
- Docker / docker-compose

If you want a local dev setup:
- python 3.6
- `virtualenv` or `virtualenvwrapper`

## Getting started
Copy the `.env-template` file:

    cp .env-template .env

Fill the variables needed:
- DATA_DIR: A path on your host where data will be written
- APP_PORT: The port you want the app to be deployed (default is 5010)

Build the docker image:

    make build

You can start the local server:

    make run-dev-server

If you kept the default `APP_PORT` variable, then you have access to the app on `localhost:5010`.







## Make commands
- `build`: will build the app image
- `run-bash`: will run a bash in the app container
- `run-prod-server`: will run the app using nginx / uwsgi
- `run-dev-server`: will run the app in debug mode (file watching and automatic restarts)


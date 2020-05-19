#! /usr/bin/env sh
set -e

export LISTEN_PORT=$PORT

/entrypoint.sh $@

#! /usr/bin/env sh
set -e

export LISTEN_PORT=$PORT

echo "$@"
/entrypoint.sh $@

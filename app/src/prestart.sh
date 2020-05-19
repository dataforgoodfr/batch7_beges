#! /usr/bin/env sh
set -e

./scripts/download_datasets.sh
python scripts/prepare_datasets.sh

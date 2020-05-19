#! /usr/bin/env sh
set -e

./scripts/download_data.sh
python scripts/prepare_datasets.sh

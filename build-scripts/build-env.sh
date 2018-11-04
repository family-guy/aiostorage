#!/usr/bin/env bash

set -xe

conda env update --name root --file dist/environment.yml
pip install --upgrade pip
pip install --requirement requirements-dev.txt
pip install --editable .

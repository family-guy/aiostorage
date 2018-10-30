#!/usr/bin/env bash

set -e

PYPI_CONFIG="~/.pypirc"
echo $'[distutils]\nindex-servers = pypi\n[pypi]' > $PYPI_CONFIG
echo "username=$PYPI_USERNAME" >> $PYPI_CONFIG
echo "password=$PYPI_PASSWORD" >> $PYPI_CONFIG
twine upload dist/*.tar.gz

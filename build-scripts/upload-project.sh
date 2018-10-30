#!/usr/bin/env bash

set -e

PYPI="~/.pypirc"
echo $'[distutils]\nindex-servers = pypi\n[pypi]' > $PYPI
echo "username=$PYPI_USERNAME" >> $PYPI
echo "password=$PYPI_PASSWORD" >> $PYPI
twine upload dist/*.tar.gz

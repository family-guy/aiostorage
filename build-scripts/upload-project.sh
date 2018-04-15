#!/usr/bin/env bash

echo "[distutils]" >> ~/.pypirc
echo "index-servers = pypi" >> ~/.pypirc
echo "[pypi]" >> ~/.pypirc
echo "username=$PYPI_USERNAME" >> ~/.pypirc
echo "password=$PYPI_PASSWORD" >> ~/.pypirc

twine upload dist/*.tar.gz

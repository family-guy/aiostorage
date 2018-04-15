#!/usr/bin/env bash

python setup.py egg_info

declare -a PIP_PACKAGES
PIP_PACKAGES=($(< aiostorage.egg-info/requires.txt))

OUTPUT=$'name: aiostorage\ndependencies:\n  - python=3.6.3\n  - pip:\n'

for PACKAGE in "${PIP_PACKAGES[@]}"
do
    OUTPUT=$OUTPUT'    - '$PACKAGE$'\n'
done

if [ ! -d dist ]; then
    mkdir -p dist
fi
cat <<EOF > dist/environment.yml
$OUTPUT
EOF

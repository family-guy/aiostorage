#!/usr/bin/env bash

python setup.py egg_info

declare -a PIP_PACKAGES
PIP_PACKAGES=($(< aiostorage.egg-info/requires.txt))

output=$'name: aiostorage\ndependencies:\n  - python=3.6.3\n  - pip:\n'

for package in "${PIP_PACKAGES[@]}"
do
    output=$output'    - '$package$'\n'
done

if [ ! -d dist ]; then
    mkdir -p dist
fi
cat <<EOF > dist/environment.yml
$output
EOF

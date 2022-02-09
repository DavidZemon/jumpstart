#!/bin/bash

set -ex

name=TestPackage
name_lower=testpackage

./jumpstart.py --defaults --name=${name} "$@"
conan install -if generated/build generated
conan build -bf generated/build generated
make -C generated/build docs package -j30

./jumpstart.py --defaults --name=${name} --no-service "$@"
conan create generated davidzemon/automatedtests
conan remove ${name_lower}/* -f

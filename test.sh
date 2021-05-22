#!/bin/bash

set -ex
rm -rf generated
./jumpstart.py --defaults "$@"
conan install -if generated/build generated
conan build -bf generated/build generated
make -C generated/build docs

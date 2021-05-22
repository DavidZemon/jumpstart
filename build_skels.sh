#!/bin/bash

set -e

docker build -t davidzemon/jumpstart .

cd ../test-conan
for directory in Skel1 Skel2 Skel3 ; do
    rm -rf "${directory}"
    mkdir "${directory}"
    pushd "${directory}"
    jumpstart --defaults --name "Jumpstarted${directory}" --namespace Zemon --no-service
    popd
done

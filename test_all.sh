#!/bin/bash

set -ex

./test.sh
./test.sh --no-library
./test.sh --no-library --no-service
./test.sh --no-executable
./test.sh --no-tests --no-library
./test.sh --no-tests --no-library --no-service
./test.sh --no-tests --no-executable
./test.sh --namespace=Zemon --no-library
./test.sh --namespace=Zemon --no-library --no-service
./test.sh --namespace=Zemon --no-executable
./test.sh --namespace=Zemon --no-tests --no-library
./test.sh --namespace=Zemon --no-tests --no-library --no-service
./test.sh --namespace=Zemon --no-tests --no-executable
./test.sh --no-cxx
./test.sh --no-cxx --no-library
./test.sh --no-cxx --no-library --no-service
./test.sh --no-cxx --no-executable
./test.sh --no-cxx --no-tests
./test.sh --no-cxx --no-tests --no-library
./test.sh --no-cxx --no-tests --no-library --no-service
./test.sh --no-cxx --no-tests --no-executable

#!/usr/bin/python3

import subprocess
from test import test

test_cases = [
    ['--no-library'],
    ['--no-library', '--no-service'],
    ['--no-executable'],
    ['--no-tests', '--no-library'],
    ['--no-tests', '--no-library', '--no-service'],
    ['--no-tests', '--no-executable'],
    ['--namespace=Zemon', '--no-library'],
    ['--namespace=Zemon', '--no-library', '--no-service'],
    ['--namespace=Zemon', '--no-executable'],
    ['--namespace=Zemon', '--no-tests', '--no-library'],
    ['--namespace=Zemon', '--no-tests', '--no-library', '--no-service'],
    ['--namespace=Zemon', '--no-tests', '--no-executable'],
    ['--no-cxx'],
    ['--no-cxx', '--no-library'],
    ['--no-cxx', '--no-library', '--no-service'],
    ['--no-cxx', '--no-executable'],
    ['--no-cxx', '--no-tests'],
    ['--no-cxx', '--no-tests', '--no-library'],
    ['--no-cxx', '--no-tests', '--no-library', '--no-service'],
    ['--no-cxx', '--no-tests', '--no-executable']
]

for case in test_cases:
    test(case)

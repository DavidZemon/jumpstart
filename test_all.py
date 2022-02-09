#!/usr/bin/python3

import os
import shutil
import subprocess
import sys
import unittest
from parameterized import parameterized
from typing import List


class JumpstartTest(unittest.TestCase):
    TEST_PACKAGE_NAME = 'JumpstartTest'

    def setUp(self):
        if os.path.exists('generated'):
            shutil.rmtree('generated')

    def tearDown(self) -> None:
        subprocess.run(['conan', 'remove', f'{self.TEST_PACKAGE_NAME.lower()}/*', '-f'])

    @parameterized.expand([
        [['--no-library']],
        [['--no-library', '--no-service']],
        [['--no-executable']],
        [['--no-tests', '--no-library']],
        [['--no-tests', '--no-library', '--no-service']],
        [['--no-tests', '--no-executable']],
        [['--namespace=Zemon', '--no-library']],
        [['--namespace=Zemon', '--no-library', '--no-service']],
        [['--namespace=Zemon', '--no-executable']],
        [['--namespace=Zemon', '--no-tests', '--no-library']],
        [['--namespace=Zemon', '--no-tests', '--no-library', '--no-service']],
        [['--namespace=Zemon', '--no-tests', '--no-executable']],
        [['--no-cxx']],
        [['--no-cxx', '--no-library']],
        [['--no-cxx', '--no-library', '--no-service']],
        [['--no-cxx', '--no-executable']],
        [['--no-cxx', '--no-tests']],
        [['--no-cxx', '--no-tests', '--no-library']],
        [['--no-cxx', '--no-tests', '--no-library', '--no-service']],
        [['--no-cxx', '--no-tests', '--no-executable']],
        [['--no-library', '--no-service']],

        # Some more test cases that exclude service but include the library to verify test_package is working
        [['--no-tests', '--no-service']],
        [['--namespace=Zemon', '--no-service']],
        [['--namespace=Zemon', '--no-tests', '--no-service']],
        [['--no-cxx', '--no-service']],
        [['--no-cxx', '--no-tests', '--no-service']]
    ])
    def test_all(self, args: List[str]):
        subprocess.run([sys.executable, './jumpstart.py', '--defaults'] + args, check=True)
        subprocess.run(['conan', 'install', '-if', 'generated/build', 'generated'], check=True)
        subprocess.run(['conan', 'build', '-bf', 'generated/build', 'generated'], check=True)
        subprocess.run(['make', '-C', 'generated/build', 'docs', 'package', '-j', '30'], check=True)

        if '--no-service' in args:
            subprocess.run([sys.executable, './jumpstart.py', '--defaults', '--name', self.TEST_PACKAGE_NAME] + args,
                           check=True)
            subprocess.run(['conan', 'create', 'generated', 'davidzemon/automatedtests'])

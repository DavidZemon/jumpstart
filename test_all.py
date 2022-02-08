#!/usr/bin/python3

import os
import shutil
import subprocess
import sys
import unittest
from parameterized import parameterized
from typing import List


class JumpstartTest(unittest.TestCase):
    def setUp(self):
        if os.path.exists('generated'):
            shutil.rmtree('generated')

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
        [['--no-cxx', '--no-tests', '--no-executable']]
    ])
    def test_all(self, args: List[str]):
        subprocess.run([sys.executable, './jumpstart.py', '--defaults'] + args, check=True)
        subprocess.run(['conan', 'install', '-if', 'generated/build', 'generated'], check=True)
        subprocess.run(['conan', 'build', '-bf', 'generated/build', 'generated'], check=True)
        subprocess.run(['make', '-C', 'generated/build', 'docs', 'package', '-j', '30'], check=True)

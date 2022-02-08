#!/usr/bin/python3

import os.path
import subprocess
import shutil
import sys
from typing import List


def test(additional_jumpstart_args: List[str]) -> None:
    if os.path.exists('generated'):
        shutil.rmtree('generated')
    subprocess.run([sys.executable, './jumpstart.py', '--defaults'] + additional_jumpstart_args, check=True)
    subprocess.run(['conan', 'install', '-if', 'generated/build', 'generated'], check=True)
    subprocess.run(['conan', 'build', '-bf', 'generated/build', 'generated'], check=True)
    subprocess.run(['make', '-C', 'generated/build', 'docs', 'package', '-j', '30'], check=True)


if __name__ == '__main__':
    test(sys.argv[1:])

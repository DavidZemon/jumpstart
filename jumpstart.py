#!/usr/bin/python3

# Copyright 2020 David Zemon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import os
import re
import shutil
import subprocess

import sys
from typing import Callable, Dict, List, Union
from distutils.spawn import find_executable

import django
from django.conf import settings
from django.template import Template, Context

from option import Option

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'generated') if 'jumpstart.py' in os.listdir('.') else os.getcwd()


def generate_type_checker(validator: Callable[[str], bool]) -> Callable[[str], str]:
    def f(value: str) -> str:
        if validator(value):
            return value
        else:
            raise argparse.ArgumentTypeError(f'{value} is an invalid option.')

    return f


def generate_regex_checker(pattern: str) -> Callable[[str], str]:
    return generate_type_checker(lambda s: re.match(pattern, s) is not None)


def validate_license_argument(f: str) -> str:
    if os.path.exists(f) and os.path.isfile(os.path.realpath(f)):
        return f
    else:
        raise argparse.ArgumentTypeError(f'{f} is not a valid path to a license template file')


OPTIONS = [
    Option('name', 'n', 'NewProject', 'Name of the new project (alphanumeric, dashes, and underscores only)',
           'Project name', generate_regex_checker('[A-Za-z]+[A-Za-z\\d_-].*')),
    Option('description', 'd', 'FIXME: This is my cool new project', 'One-sentence description of the project',
           'Description'),
    Option('contact', 'c', 'First Last <first.last@fakery.com>',
           'Contact name and email address for package maintainer', 'Package maintainer contact',
           generate_regex_checker('\\w+ \\w+ <[^@\\s]+@[^@\\s]+\\.[^@\\s]{2,4}>')),
    Option('copyright', None, 'Your Company, Inc.', 'Your name or your company\'s name (used in copyright notice)',
           'Copyright'),
    Option('namespace', None, 'YourNamespace',
           'A short name or acronym, indicating the namespace & header directory for this project', 'Namespace'),
    Option('homepage', None, 'https://github.com/YourCompany/new-project', 'Homepage for your project', 'Homepage'),
    Option('cxx', None, True, 'Disable C++ support (C++ is always enabled for unit tests)',
           'Should C++ support be enabled in the primary targets (C++ is always enabled for unit tests)'),
    Option('library', 'l', True, 'When enabled, a default library target will be created.',
           'Should a default library target be created'),
    Option('executable', 'e', True, 'When enabled, a default executable target will be created.',
           'Should a default executable target be created'),
    Option('service', 's', True, 'When enabled and combined with --executable, a sample init script will be created.',
           'Should a sample init script be included for use as a service (Only applicable when an executable is being '
           'created)'),
    Option('tests', 't', True, 'Disable unit test support', 'Should unit test support be included'),
    Option('license', None, os.path.join(BASE_DIR, 'LicenseTemplate.txt'),
           'Path to custom license text. See default license file for placeholder syntax.', 'License path',
           validate_license_argument)
]
# These are files that I do not wish to have copies of in VCS, but also do not want to create symlinks for due to
# Windows compatibility. However, the content of the file may end up in two different directories, depending on options.
# The dictionary is in the form {DESTINATION: SOURCE}
LINKS = {
    'src/@name@.h': os.path.join(TEMPLATES_DIR, 'include/@namespace@/@name@.h')
}


def run() -> None:
    settings.configure(TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'APP_DIRS': False}])
    django.setup()

    args = parse_args()
    final_options = get_options(args)

    if final_options['name'].lower() == 'test':
        raise Exception('"test" (any combination of case) is a reserved word in CMake and can not be used as a '
                        'project name.')

    blacklist = get_blacklisted_files(final_options)

    # Handle the case where the output directory already exists
    move_license_file = False
    if os.path.exists(OUTPUT_DIR):
        existing_files = os.listdir(OUTPUT_DIR)
        if existing_files:
            if OUTPUT_DIR == os.path.join(os.getcwd(), 'generated'):
                shutil.rmtree(OUTPUT_DIR)
            else:
                # If the only existing file is the input license file, that's okay because that's the only easy way to
                # provide a license when run via Docker

                existing_file = os.path.join(OUTPUT_DIR, existing_files[0])
                input_license = final_options['license']
                if len(existing_files) == 1 and os.path.samefile(existing_file, input_license):
                    move_license_file = True
                else:
                    raise Exception('An input license file is the only file allow in the output directory. Please empty'
                                    ' it or create a new directory.')

    # Write all template files to output directory
    for root, dirs, filenames in os.walk(TEMPLATES_DIR):
        for filename in filenames:
            abs_path_in = os.path.join(root, filename)
            if all(not abs_path_in.endswith(b) for b in blacklist):  # Should not be in blacklist
                relative_to_templates = abs_path_in[len(TEMPLATES_DIR) + 1:]
                write_file(abs_path_in, relative_to_templates, final_options)

    # Write all "linked" files to output directory
    for destination, source in LINKS.items():
        abs_path_in = os.path.join(TEMPLATES_DIR, source)
        if all(not destination.endswith(b) for b in blacklist):  # Should not be in blacklist
            write_file(abs_path_in, destination, final_options)

    # Write license file
    if move_license_file:
        # If the input license file is not named 'LICENSE', using `write_file()` would leave the original license file
        # behind. It would then get included (duplicated) in the initial Git commit.
        tmp_license_filepath = '/tmp/input_license'
        shutil.copyfile(final_options['license'], tmp_license_filepath)
        os.remove(final_options['license'])
        try:
            write_file(tmp_license_filepath, 'LICENSE', final_options)
        except BaseException:
            # If anything goes wrong, be sure to put the input file back
            shutil.copyfile(tmp_license_filepath, final_options['license'])
            raise
    else:
        write_file(final_options['license'], 'LICENSE', final_options)

    # Initialize Git repo and perform first commit
    git_exe = find_executable('git')
    if git_exe:
        subprocess.check_output(['git', 'init', '--initial-branch', 'main'], cwd=OUTPUT_DIR)
        subprocess.check_output(['git', 'add', '.'], cwd=OUTPUT_DIR)
        subprocess.check_output([
            'git',
            '-c', 'user.name=Jumpstart Generator',
            '-c', 'user.email=noreply@jumpstart.nowhere',
            'commit', '-m', 'Generated from jumpstart'
        ], cwd=OUTPUT_DIR)
    else:
        print('WARNING: git not found. Please run `git init && git add . && git commit` to initialize your repository.',
              file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    for option in OPTIONS:
        if isinstance(option.default_value, bool):
            if option.default_value:
                parser.add_argument('--no-' + option.long_name, action='store_const', const=False,
                                    dest=option.long_name.replace('-', '_'), help=option.cli_help)
            else:
                parser.add_argument('--' + option.long_name, action='store_const', const=True, help=option.cli_help)
        elif option.short_name:
            parser.add_argument('-' + option.short_name, '--' + option.long_name, type=option.validator,
                                help=option.cli_help)
        else:
            parser.add_argument('--' + option.long_name, type=option.validator,
                                help=option.cli_help)

    parser.add_argument('--defaults', action='store_true',
                        help='Do not prompt any questions - use default values for any option not provided on the '
                             'command line.')

    return parser.parse_args()


def get_options(args: argparse.Namespace) -> Dict[str, Union[str, bool]]:
    final_options: Dict[str, Union[str, bool]] = {}

    for option in OPTIONS:
        dest = option.long_name.replace('-', '_')
        if args.__getattribute__(dest) is None:
            if args.defaults:
                final_options[dest] = option.default_value
            else:
                while dest not in final_options:
                    response = input(option.interactive_prompt)
                    if '' == response:
                        if option.default_value:
                            final_options[dest] = option.default_value
                        else:
                            print('No default value available for ' + option.long_name)
                    elif option.type == bool:
                        if response.lower() in ['y', 'yes', 't', 'true', '1']:
                            final_options[dest] = True
                        elif response.lower() in ['n', 'no', 'f', 'false', '0']:
                            final_options[dest] = False
                        else:
                            print('Expected one of y, yes, n, or no.')
                    else:
                        final_options[dest] = response

                    if dest in final_options and option.validator:
                        try:
                            option.validator(final_options[dest])
                        except argparse.ArgumentTypeError as e:
                            print(e)
                            del final_options[dest]
        else:
            final_options[dest] = args.__getattribute__(dest)

    final_options.update(get_computed_options(final_options))

    return final_options


def get_computed_options(options: Dict[str, Union[str, bool]]) -> Dict[str, Union[str, bool]]:
    results = {}

    if options['executable']:
        results['lib_target_name'] = options['name'].lower() + '-lib'
    else:
        results['lib_target_name'] = options['name'].lower()

    if options['cxx']:
        results['extension'] = '.cpp'
        results['test_package_name'] = 'GMock'
    else:
        results['extension'] = '.c'
        results['test_package_name'] = 'GTest'

    results['service'] = options['service'] and options['executable']

    # Compute license text
    filename = options['license']
    with open(filename, 'r') as f:
        content = f.read()
        license_template_text = content.strip()
        results['license_text'] = Template(license_template_text).render(Context(options))
    results['license_text_for_script'] = os.linesep.join(['# ' + line for line in results['license_text'].splitlines()])
    results['license_text_for_cxx'] = os.linesep.join([' * ' + line for line in results['license_text'].splitlines()])

    return results


def get_blacklisted_files(options: Dict[str, any]) -> List[str]:
    blacklist = []
    if not options['executable']:
        blacklist.append('main@extension@')
        blacklist.append('@name@-cli@extension@')
        blacklist.append('@name@-cli.h')
    if not options['cxx']:
        blacklist.append('FindGMock.cmake')
    if options['library']:
        blacklist.append('src/@name@.h')  # Only include one of these headers, never both
    else:
        blacklist.append('@namespace@/@name@.h')
        blacklist.append('test_package/@name@TestConan.cpp')
        blacklist.append('test_package/CMakeLists.txt')
        blacklist.append('test_package/conanfile.py')
    if not options['tests']:
        blacklist.append('CMakeModules/FindGMock.cmake')
        blacklist.append('tests/@name@-cliTest.cpp')
        blacklist.append('tests/@name@Test.cpp')
        blacklist.append('tests/CMakeLists.txt')
    if not options['tests'] and not options['library']:
        blacklist.append('src/@name@@extension@')
        blacklist.append('src/@name@.h')
        blacklist.append('src/@name@-cli@extension@')
        blacklist.append('src/@name@-cli.h')
    if not options['service']:
        blacklist.append('scripts/@name@.init')
    return blacklist


def write_file(abs_path_in: str, relative_output_path: str, options: Dict[str, any]) -> None:
    try:
        with open(abs_path_in, 'r') as f:
            t = Template(f.read())
    except Exception as e:
        raise Exception(f'Failed to process template file {abs_path_in}') from e

    abs_path_out = os.path.join(OUTPUT_DIR, relative_output_path)
    abs_path_out = adjust_output_filename(abs_path_out, options)
    abs_dir_out = os.path.dirname(abs_path_out)
    os.makedirs(abs_dir_out, exist_ok=True)

    content = t.render(Context(options, autoescape=False)).rstrip()
    stripped_lines = [f'{line.rstrip()}{os.linesep}' for line in content.split(os.linesep)]

    with open(abs_path_out, 'w') as f:
        f.writelines(stripped_lines)


def adjust_output_filename(unmolested: str, options: Dict[str, any]) -> str:
    result = unmolested
    for k, v in options.items():
        result = result.replace(f'@{k}@', str(v))
    return result


def echo_run(args, cwd) -> None:
    subprocess.check_output(args, cwd=cwd)


if '__main__' == __name__:
    run()

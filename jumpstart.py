#!/usr/bin/python3
import argparse
import os
import re
import shutil
from typing import Callable, Dict, List

import django
from django.conf import settings
from django.template import Template, Context

from option import Option

TEMPLATES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'generated') if 'jumpstart.py' in os.listdir('.') else os.getcwd()


def generate_type_checker(validator: Callable[[str], bool]) -> Callable[[str], str]:
    def f(value: str) -> str:
        if validator(value):
            return value
        else:
            raise argparse.ArgumentTypeError('{0} is an invalid option.'.format(value))

    return f


def generate_regex_checker(pattern: str) -> Callable[[str], str]:
    return generate_type_checker(lambda s: re.match(pattern, s) is not None)


OPTIONS = [
    Option('name', 'n', 'NewProject', 'Name of the new project (alphanumeric, dashes, and underscores only)',
           'Project name', generate_regex_checker('[A-Za-z]+[A-Za-z\d_-].*')),
    Option('description', 'd', 'FIXME: This is my cool new project', 'One-sentence description of the project',
           'Description'),
    Option('contact', 'c', 'First Last <first.last@redlion.net>',
           'Contact name and email address for package maintainer', 'Contact name',
           generate_regex_checker('[A-Za-z]+ [A-Za-z]+ <[a-z\d\.]+@redlion\.net>')),
    Option('cxx', None, True, 'Disable C++ support (C++ is always enabled for unit tests)',
           'Should C++ support be enabled in the primary targets (C++ is always enabled for unit tests)'),
    Option('library', 'l', True, 'When enabled, a default library target will be created.',
           'Should a default library target be created'),
    Option('executable', 'e', True, 'When enabled, a default executable target will be created.',
           'Should a default executable target be created')
]


def run() -> None:
    settings.configure(TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'APP_DIRS': False}])
    django.setup()

    args = parse_args()
    final_options = get_options(args)

    if final_options['name'].lower() == 'test':
        raise Exception('"test" (any combination of case) is a reserved word in CMake and can not be used as a '
                        'project name.')

    blacklist = get_blacklisted_files(final_options)

    if os.listdir(OUTPUT_DIR):
        if OUTPUT_DIR == os.path.join(os.getcwd(), 'generated'):
            shutil.rmtree(OUTPUT_DIR)
        else:
            raise Exception('Current directory MUST be empty. Please empty it or create a new directory.')

    for root, dirs, filenames in os.walk(TEMPLATES_DIR):
        for filename in filenames:
            abs_path_in = os.path.join(root, filename)
            if all(not abs_path_in.endswith(b) for b in blacklist):  # Should not be in blacklist
                relative_to_templates = abs_path_in[len(TEMPLATES_DIR) + 1:]
                with open(abs_path_in, 'r') as f:
                    t = Template(f.read())

                abs_path_out = os.path.join(OUTPUT_DIR, relative_to_templates)
                abs_path_out = adjust_output_filename(abs_path_out, final_options)
                abs_dir_out = os.path.dirname(abs_path_out)
                os.makedirs(abs_dir_out, exist_ok=True)
                with open(abs_path_out, 'w') as f:
                    f.write(t.render(Context(final_options)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    for option in OPTIONS:
        if isinstance(option.default_value, bool):
            if option.default_value:
                parser.add_argument('--no-' + option.long_name, action='store_const', const=False,
                                    dest=option.long_name.replace('-', '_'), help=option.cli_help)
            else:
                parser.add_argument('--' + option.long_name, action='store_const', const=True, help=option.cli_help)
        else:
            parser.add_argument('-' + option.short_name, '--' + option.long_name, type=option.validator,
                                help=option.cli_help)

    parser.add_argument('--defaults', action='store_true', help='Use all default. Do not prompt any questions.')

    return parser.parse_args()


def get_options(args: argparse.Namespace) -> Dict[str, any]:
    final_options = {}

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


def get_computed_options(options: Dict[str, any]) -> Dict[str, any]:
    results = {}

    if options['library'] and options['executable']:
        results['lib_target_name'] = options['name'].lower() + '-lib'
    else:
        results['lib_target_name'] = options['name'].lower()

    if options['cxx']:
        results['extension'] = '.cpp'
        results['test_package_name'] = 'GMock'
    else:
        results['extension'] = '.c'
        results['test_package_name'] = 'GTest'

    return results


def get_blacklisted_files(options: Dict[str, any]) -> List[str]:
    blacklist = []
    if not options['executable']:
        blacklist.append('main@extension@')
        blacklist.append('@name@-cli@extension@')
        blacklist.append('@name@-cli.h')
    if not options['cxx']:
        blacklist.append('FindGMock.cmake')
    if not options['library']:
        blacklist.append('test_package/@name@TestConan.cpp')
        blacklist.append('test_package/CMakeLists.txt')
        blacklist.append('test_package/conanfile.py')
    return blacklist


def adjust_output_filename(unmolested: str, options: Dict[str, any]) -> str:
    result = unmolested
    for k, v in options.items():
        result = result.replace('@{0}@'.format(k), str(v))
    return result


if '__main__' == __name__:
    run()

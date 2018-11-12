#!/usr/bin/python3
import os
import argparse
import re

from string import Template
from typing import Union, Callable, Type, Dict

TEMPLATES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')


def generate_type_checker(validator: Callable[[str], bool]):
    def f(value: str) -> str:
        if validator(value):
            return value
        else:
            raise argparse.ArgumentTypeError('{0} is an invalid option.'.format(value))
    return f


class Option(object):
    def __init__(self, name: str, short_name: Union[str, None], default_value, cli_help: str, interactive_prompt: str,
                 validator: Callable[[str], any] = None, value_type: Type = None):
        self.long_name = name
        self.short_name = short_name
        self.default_value = default_value
        if value_type is not None:
            self.type = value_type
        else:
            self.type = type(self.default_value)
        self.value = default_value
        self.cli_help = cli_help
        if default_value is not None:
            if isinstance(default_value, bool):
                if default_value:
                    self.interactive_prompt = '{0} [Y/n]: '.format(interactive_prompt)
                else:
                    self.interactive_prompt = '{0} [y/N]: '.format(interactive_prompt)
            else:
                self.interactive_prompt = '{0} [{1}]: '.format(interactive_prompt, default_value)
        else:
            self.interactive_prompt = '{0}: '.format(interactive_prompt)
        self.validator = validator


OPTIONS = [
    Option('name', 'n', 'NewProject', 'Name of the new project (alphanumeric, dashes, and underscores only)',
           'Project name', generate_type_checker(lambda s: re.match('[A-Za-z]+[A-Za-z\d_-].*', s) is not None)),
    Option('cxx', None, True, 'Disable C++ support (C++ is always enabled for unit tests)',
           'Should C++ support be enabled in the primary targets (C++ is always enabled for unit tests)')
]


def run() -> None:
    args = parse_args()
    final_options = get_options(args)
    print(final_options)


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

    return parser.parse_args()


def get_options(args: argparse.Namespace) -> Dict[str, any]:
    final_options = {}

    for option in OPTIONS:
        dest = option.long_name.replace('-', '_')
        if args.__getattribute__(dest) is None:
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

                if dest in final_options and option.validator and not option.validator(final_options[dest]):
                    print('"{0}" is not a valid option.'.format(final_options[dest]))
                    del final_options[dest]
        else:
            final_options[dest] = args.__getattribute__(dest)

    return final_options


if '__main__' == __name__:
    run()

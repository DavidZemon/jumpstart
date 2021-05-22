from typing import Union, Callable, Type


class Option(object):
    def __init__(self, name: str, short_name: Union[str, None], default_value: Union[str, bool], cli_help: str,
                 interactive_prompt: str, validator: Callable[[str], any] = None, value_type: Type = None):
        self.long_name = name
        self.short_name = short_name
        self.default_value = default_value
        if value_type is not None:
            self.type = value_type
        else:
            self.type = type(self.default_value)
        self.value = default_value
        self.cli_help = cli_help
        if isinstance(default_value, bool):
            if default_value:
                self.interactive_prompt = '{0} [Y/n]: '.format(interactive_prompt)
            else:
                self.interactive_prompt = '{0} [y/N]: '.format(interactive_prompt)
        else:
            self.interactive_prompt = '{0} [{1}]: '.format(interactive_prompt, default_value)
        self.validator = validator

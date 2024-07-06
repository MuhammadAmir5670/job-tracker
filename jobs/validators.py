import re

from django.core.exceptions import ValidationError


def valid_regex(value):
    try:
        re.compile(value)
    except re.error as error:
        ValidationError(f"'{value}' is not a valid regular expression. | {error.message}")

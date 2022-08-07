import logging
import re
from typing import List, Union

logger = logging.getLogger(__name__)


class ParameterError(Exception):
    pass


def _check_patterns(patterns: List[Union[str, tuple]], string_to_check: Union[str, dict]) -> bool:
    """
    :param patterns: regular expressions or a tuple
    :type patterns: a lists of strings or tuples
    :param string_to_check: string or a dictionary to be matched
    :type string_to_check:
    :return: true if matched
    :rtype: bool
    helper function for matching regular expressions.
    if pattern is a tuple, the regular expression is element one and element zero is the key of a dictionary where
    the value is the string to be matched
    """
    if string_to_check is None:
        return False
    elif not isinstance(string_to_check, (str, dict)):
        logger.error("_check_patterns: failure: string_to_check wrong type {}".format(string_to_check))
        raise ParameterError("string_to_check must be a string or a dictionary")
    if isinstance(patterns, (list, tuple)):
        for pattern in patterns:
            if isinstance(pattern, str):
                pattern = re.compile(pattern, re.MULTILINE)
                if pattern.search(string_to_check):
                    return True
            elif isinstance(pattern, (list, tuple)):
                pattern = re.compile(pattern[1], re.MULTILINE)
                if pattern.search(string_to_check[pattern[0]]):
                    return True
            else:
                logger.error("_check_patterns: failure: pattern {}, string {}".format(pattern, string_to_check))
                raise ParameterError("pattern must be a string or tuple of two strings")
    else:
        logger.error("_check_patterns: patterns wrong type {}".format(patterns))
        raise ParameterError("patterns must be a list or tuple")
    return False
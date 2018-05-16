#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# Dive - Media content finder tool
# Common core module
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/dive
# ============================================================================

__version__ = "2.1.3"

from . import paval as pv
import re

def compile_regex(string, ignore_case=True, regex_syntax=False):
    """
        Compile a regular expression from the given string.
    """
    pv.string(string, "regular expression", True, None)

    # Either use the professional way (regex syntax) or the simplified way
    # (only supports an asterisk as wildcard and semicolon as a seperator)
    if regex_syntax:
        pattern = ".*" + string + ".*"
    else:
        pattern = ""
        spec_chars = [ "\\", ".", "^", "$", "+", "?", "{", "}", "[", "]", "|",
                       "(", ")" ]

        for char in spec_chars:
            string = string.replace(char, "\\" + char)

        string = string.strip("*")
        string = string.strip(";")

        while ("*" * 2) in string:
            string = string.replace(("*" * 2), "*")

        while (";" * 2) in string:
            string = string.replace((";" * 2), ";")

        list_string = string.split(";")
        for string in list_string:
            if not string == "":
                pattern += "(.*" + string.replace("*", ".*") + ".*)|"
        pattern = pattern.rstrip("|")

        if pattern == "":
            raise Exception("The given string does not make sense this way.")

    if ignore_case:
        regex = re.compile(pattern, re.IGNORECASE)
    else:
        regex = re.compile(pattern)

    return regex

def get_max_digits(numbers):
    """
        Return the amount of digits of the largest number.
    """
    list_digits = []

    for item in numbers:
        list_digits.append(int(len(str(item))))

    return int(max(list_digits))

def get_version():
    """
        Return the version of this module.
    """
    return __version__

# EOF


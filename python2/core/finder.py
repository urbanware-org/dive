#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# Dive - Media content finder tool
# Content File core module
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/dive
# ============================================================================

__version__ = "2.1.3"

import common
import os
import paval as pv

def find_term(content_file, search_term, ignore_case=True,
              regex_syntax=False):
    """
        Search a content file for the given search term.
    """
    pv.path(content_file, "content file", True, True)
    pv.string(search_term, "search term", True, None)

    content_file = os.path.abspath(content_file)
    list_matches = []
    regex = common.compile_regex(search_term, ignore_case, regex_syntax)

    fh_content = open(content_file, "r")
    for line in fh_content:
        if ignore_case:
            if regex.match(line.lower()):
                list_matches.append(line.replace("\n", ""))
        else:
            if regex.match(line):
                list_matches.append(line.replace("\n", ""))

    fh_content.close()
    list_matches.sort()

    return list_matches

def get_files(directory):
    """
        Get all content files which are stored in the given directory.
    """
    pv.path(directory, "content file", False, True)
    directory = os.path.abspath(directory)

    list_files = []
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.exists(path) and os.path.isfile(path):
            if path.endswith(".dcl"):
                list_files.append(path)
    list_files.sort()

    if len(list_files) > 0:
        return list_files
    else:
        raise Exception("No content files found inside the given " + \
                        "directory.")

def get_version():
    """
        Return the version of this module.
    """
    return __version__

# EOF


#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# Dive - Media content finder tool
# Content File Builder core module
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/dive
# ============================================================================

__version__ = "2.1.3"

import common
import deepdive
import os
import paval as pv

def build_content_file(dir_destination, content_file, dir_source,
                       ignore_read_errors=False, pattern_exclude=None,
                       ignore_exclude_case=True, regex_syntax=False,
                       bin_unace=None, bin_unrar=None, read_tar=False,
                       read_zip=False, replace_string=None):
    """
        Create a content file from the given directory.
    """
    pv.path(dir_destination, "destination", False, True)
    pv.path(dir_source, "source", False, True)
    pv.path(content_file, "content", True, False)

    dir_destination = os.path.abspath(dir_destination)
    dir_source = os.path.abspath(dir_source)

    if not dir_destination.endswith(os.sep):
        dir_destination += os.sep
    if not dir_source.endswith(os.sep):
        dir_source += os.sep

    regex = None
    if not pattern_exclude == None:
        regex = common.compile_regex(pattern_exclude, ignore_exclude_case,
                                     regex_syntax)

    content_file_path = os.path.join(dir_destination, content_file)
    if not content_file_path.endswith(".dcl"):
        content_file_path += ".dcl"

    if os.path.exists(content_file_path):
        if os.path.isfile(content_file_path):
            raise Exception("The given content file already exists.")
        elif os.path.isdir(content_file_path):
            raise Exception("The given content file path does not seem " + \
                            "to be a file.")

    stats = __build_content_file(content_file_path, dir_source,
                                 ignore_read_errors, regex,
                                 ignore_exclude_case, bin_unace, bin_unrar,
                                 read_tar, read_zip, replace_string)

    return stats

def get_version():
    """
        Return the version of this module.
    """
    return __version__

def __build_content_file(content_file, dir_source, ignore_read_errors, regex,
                         ignore_exclude_case, bin_unace, bin_unrar, read_tar,
                         read_zip, replace_string):
    """
        Core method to create a content file.
    """
    list_content = []
    line = ""
    lines_archive = 0
    lines_excluded = 0
    lines_ignored = 0
    lines_written = 0
    read_ace = False
    read_rar = False

    if not bin_unace == None:
        pv.path(bin_unace, "UnACE binary", True, True)
        bin_unace = os.path.abspath(bin_unace)
        read_ace = True
    if not bin_unrar == None:
        pv.path(bin_unrar, "UnRAR binary", True, True)
        bin_unrar = os.path.abspath(bin_unrar)
        read_rar = True

    if read_ace or read_rar or read_tar or read_zip:
        use_deepdive = True
    else:
        use_deepdive = False

    list_content, lines_ignored = \
         __get_content(dir_source, ignore_read_errors, list_content,
                       lines_ignored)
    list_content.sort()

    if not len(list_content) > 0:
        raise Exception("No content to gather in the given directory.")

    fh_content = open(content_file, "w")
    for item in list_content:
        if regex == None:
            line = __prepare_line(item, dir_source, replace_string)
            lines_written += 1
        else:
            if ignore_exclude_case:
                if regex.match(item.lower()):
                    lines_excluded += 1
                    continue
                else:
                    line = __prepare_line(item, dir_source, replace_string)
                    lines_written += 1
            else:
                if regex.match(item):
                    lines_excluded += 1
                    continue
                else:
                    line = __prepare_line(item, dir_source, replace_string)
                    lines_written += 1

        if not use_deepdive:
            fh_content.write(line + "\n")
        else:
            content = None
            read_error = False
            if read_ace:
                if item.lower().endswith(".ace"):
                    content, read_error = \
                        deepdive.get_content_ace(item, bin_unace,
                                                 ignore_read_errors)
            if read_rar:
                if item.lower().endswith(".rar"):
                    content, read_error = \
                        deepdive.get_content_rar(item, bin_unrar,
                                                 ignore_read_errors)
            if read_tar:
                if item.lower().endswith(".tar") or \
                   item.lower().endswith(".tar.bz2") or \
                   item.lower().endswith(".tar.gz") or \
                   item.lower().endswith(".tgz"):
                    content, read_error = \
                        deepdive.get_content_tar(item, ignore_read_errors)
            if read_zip:
                if item.lower().endswith(".zip"):
                    content, read_error = \
                        deepdive.get_content_zip(item, ignore_read_errors)

            if content == None:
                if read_error:
                    fh_content.write(line + " [?]" + "\n")
                    lines_ignored += 1
                else:
                    fh_content.write(line + "\n")
                continue
            else:
                fh_content.write(line + "\n")
                for subitem in content:
                    if regex == None:
                        line = __prepare_line(subitem, dir_source,
                                              replace_string)
                        lines_archive += 1
                        lines_written += 1
                    else:
                        if ignore_exclude_case:
                            if regex.match(subitem.lower()):
                                lines_archive += 1
                                lines_excluded += 1
                                continue
                            else:
                                line = __prepare_line(subitem, dir_source,
                                                      replace_string)
                                lines_archive += 1
                                lines_written += 1
                        else:
                            if regex.match(subitem):
                                lines_archive += 1
                                lines_excluded += 1
                                continue
                            else:
                                line = __prepare_line(subitem, dir_source,
                                                      replace_string)
                                lines_archive += 1
                                lines_written += 1

                    fh_content.write(line + "\n")

    fh_content.close()
    lines_total = len(list_content)

    stats = {"lines_archive": lines_archive,
             "lines_excluded": lines_excluded,
             "lines_ignored": lines_ignored,
             "lines_total": lines_total,
             "lines_written": lines_written}

    return stats

def __get_content(directory, ignore_read_errors, list_content, lines_ignored):
    """
        Gather the content for building the content file.
    """
    pv.path(directory, "source directory", False, True)

    directory = os.path.abspath(directory)
    ignored = 0
    list_dirs = []

    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            list_content.append(path)
        else:
            list_content.append(path)
            list_dirs.append(path)

    for directory in list_dirs:
        try:
            content, ignored = \
                __get_content(directory, ignore_read_errors, list_content,
                              lines_ignored)
        except:
            if ignore_read_errors:
                lines_ignored += (ignored + 1)
            else:
                raise Exception("Unable to read the contents of the " \
                                "directory \"%s\" (maybe a permission " \
                                "problem)." % directory)

    return list_content, lines_ignored

def __prepare_line(string, dir_source, replace_string):
    """
        Prepare the line before it is being written into the content file
    """
    if not replace_string == None:
        string = string.replace(dir_source, replace_string)

    return string

# EOF


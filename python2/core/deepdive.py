#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# Dive - Media content finder tool
# Deep Dive core module
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/dive
# ============================================================================

__version__ = "2.1.3"

import os
import paval as pv
import subprocess
import tarfile
import zipfile


def get_content_ace(archive, bin_unace, ignore_read_errors):
    """
        Get the contents of an ACE archive file (requires "unace" tool).
    """
    pv.path(archive, "archive", True, True)
    pv.path(bin_unace, "UnACE binary", True, True)

    archive = os.path.abspath(archive)
    bin_unace = os.path.abspath(bin_unace)
    read_error = False

    try:
        archive_content = __get_content_ace(archive, bin_unace)
    except:
        if ignore_read_errors:
            archive_content = None
            read_error = True
        else:
            raise Exception("Unable to read the contents of the ACE " \
                            "archive \"%s\" (maybe a permission problem)." \
                            % archive)

    return archive_content, read_error

def get_content_rar(archive, bin_unrar, ignore_read_errors):
    """
        Get the contents of a RAR archive file (requires "unrar" tool).
    """
    pv.path(archive, "archive", True, True)
    pv.path(bin_unrar, "UnRAR binary", True, True)

    archive = os.path.abspath(archive)
    bin_unrar = os.path.abspath(bin_unrar)
    read_error = False

    try:
        archive_content = __get_content_rar(archive, bin_unrar)
    except:
        if ignore_read_errors:
            archive_content = None
            read_error = True
        else:
            raise Exception("Unable to read the contents of the RAR " \
                            "archive \"%s\" (maybe a permission problem)." \
                            % archive)

    return archive_content, read_error

def get_content_tar(archive, ignore_read_errors):
    """
        Get the contents of a TAR archive file.
    """
    pv.path(archive, "archive", True, True)

    read_error = False

    try:
        archive_content = __get_content_tar(os.path.abspath(archive))
    except:
        if ignore_read_errors:
            archive_content = None
            read_error = True
        else:
            raise Exception("Unable to read the contents of the TAR " \
                            "archive \"%s\" (maybe a permission problem)." \
                            % archive)

    return archive_content, read_error

def get_content_zip(archive, ignore_read_errors):
    """
        Get the contents of a ZIP archive file.
    """
    pv.path(archive, "archive", True, True)

    read_error = False

    try:
        archive_content = __get_content_zip(os.path.abspath(archive))
    except:
        if ignore_read_errors:
            archive_content = None
            read_error = True
        else:
            raise Exception("Unable to read the contents of the ZIP " \
                            "archive \"%s\" (maybe a permission problem)." \
                            % archive)

    return archive_content, read_error

def get_version():
    """
        Return the version of this module.
    """
    return __version__

def __get_content_ace(archive, bin_unace):
    """
        Core method to get the contents of an ACE archive file.
    """
    archive_content = []
    archive = os.path.abspath(archive)
    bin_unace = os.path.abspath(bin_unace)

    output = subprocess.check_output([bin_unace, "l", "-c-", archive])
    lines = output.split("\n")
    for line in lines:
        if not line == "":
            if "%" in line:
                temp_line = line.replace("\xb3", "")
                temp_list = temp_line.split("%")
                file_name = temp_list[-1].lstrip()
                archive_content.append(archive + ":" + file_name)
    archive_content.sort()

    return archive_content

def __get_content_rar(archive, bin_unrar):
    """
        Core method to get the contents of a RAR archive file.
    """
    archive_content = []
    archive = os.path.abspath(archive)
    bin_unrar = os.path.abspath(bin_unrar)

    output = subprocess.check_output([bin_unrar, "lb", "-c-", archive])
    lines = output.split("\n")
    for line in lines:
        if not line == "":
            archive_content.append(archive + ":" + line)
    archive_content.sort()

    return archive_content

def __get_content_tar(archive):
    """
        Core method to get the contents of a TAR archive file.
    """
    archive_content = []
    archive = os.path.abspath(archive)

    t = tarfile.open(archive, "r")
    for filename in t.getnames():
        archive_content.append(archive + ":" + filename)
    archive_content.sort()

    return archive_content

def __get_content_zip(archive):
    """
        Core method to get the contents of a ZIP archive file.
    """
    archive_content = []
    archive = os.path.abspath(archive)

    z = zipfile.ZipFile(archive, "r")
    for filename in z.namelist():
        archive_content.append(archive + ":" + filename)
    archive_content.sort()

    return archive_content

# EOF


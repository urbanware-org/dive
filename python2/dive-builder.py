#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# Dive - Media content finder tool
# Content File Builder script
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/dive
# ============================================================================

import os
import sys

def main():
    from core import builder
    from core import clap
    from core import common

    try:
        p = clap.Parser()
    except Exception as e:
        print "%s: error: %s" % (os.path.basename(sys.argv[0]), e)
        sys.exit(1)

    p.set_description("Create a content file from a directory or media.")
    p.set_epilog("Further information and usage examples can be found " \
                 "inside the documentation file for this script.")

    # Define required arguments
    p.add_avalue("-d", "--destination-directory", "destination directory " \
                 "(where to create the content file in)", "dir_destination",
                 None, True)
    p.add_avalue("-f", "--content-file", "name of the content file to create",
                 "content_file", None, True)
    p.add_avalue("-s", "--source-directory", "source directory (from which " \
                 "to gather the contents)", "dir_source", None, True)

    # Define optional arguments
    p.add_switch("-c", "--case-sensitive", "do not ignore the case of the " \
                 "given exclude pattern", "case", False, False)
    p.add_avalue("-e", "--exclude", "pattern to exclude certain files or " \
                 "directories from the content file (case-insensitive, " \
                 "multiple patterns separated via semicolon)",
                 "pattern_exclude", None, False)
    p.add_switch("-h", "--help", "print this help message and exit", None,
                 True, False)
    p.add_switch("-i", "--ignore-read-errors", "ignore read errors while " \
                 "gathering content", "ignore_read_errors", True, False)
    p.add_avalue(None, "--include-ace", "include the content from ACE " \
                 "archive files (requires 'unace' binary)", "bin_unace",
                 None, False)
    p.add_avalue(None, "--include-rar", "include the content from RAR " \
                 "archive files (requires 'unrar' binary)", "bin_unrar",
                 None, False)
    p.add_switch(None, "--include-tar", "include the content from TAR " \
                 "archive files (also supports Bzip2 and Gzip compressed " \
                 "TAR archives)", "include_tar", True, False)
    p.add_switch(None, "--include-zip", "include the content from ZIP " \
                 "archive files", "include_zip", True, False)
    p.add_switch(None, "--regex", "use regex syntax for the search term " \
                 "instead of just asterisk wildcards and semicolon " \
                 "separators (for details see the section \"Regular " \
                 "expression operations\" inside the Python documentation)",
                 "regex", True, False)
    p.add_avalue("-r", "--replace-source-directory", "replace the source " \
                 "directory path with a user-defined string inside the " \
                 "content file", "replace_string", None, False)
    p.add_switch(None, "--version", "print the version number and exit", None,
                 True, False)

    if len(sys.argv) == 1:
        p.error("At least one required argument is missing.")
    elif ("-h" in sys.argv) or ("--help" in sys.argv):
        p.print_help()
        sys.exit(0)
    elif "--version" in sys.argv:
        print builder.get_version()
        sys.exit(0)

    args = p.parse_args()
    try:
        if args.ignore_read_errors == None:
            args.ignore_read_errors = False

        print
        print "Building the content file. Please wait."

        stats = builder.build_content_file(args.dir_destination,
                                           args.content_file, args.dir_source,
                                           args.ignore_read_errors,
                                           args.pattern_exclude, args.case,
                                           args.regex, args.bin_unace,
                                           args.bin_unrar, args.include_tar,
                                           args.include_zip,
                                           args.replace_string)

        just = common.get_max_digits([str(stats["lines_archive"]),
                                      str(stats["lines_excluded"]),
                                      str(stats["lines_ignored"]),
                                      str(stats["lines_total"]),
                                      str(stats["lines_written"])])

        print "Build process completed."
        print
        print "Total gathered lines of content:   %s" % \
              str(stats["lines_total"]).rjust(just, " ")
        print "Total lines read from archives:    %s" % \
              str(stats["lines_archive"]).rjust(just, " ")
        print "Total lines excluded from file:    %s" % \
              str(stats["lines_excluded"]).rjust(just, " ")
        print "Total amount of read errors:       %s" % \
              str(stats["lines_ignored"]).rjust(just, " ")
        print
        print "Total lines written into file:     %s" % \
              str(stats["lines_written"]).rjust(just, " ")
        print
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF


#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# Dive - Media content finder tool
# Content Finder script
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/dive
# ============================================================================

import os
import sys

def main():
    from core import clap
    from core import common
    from core import finder

    try:
        p = clap.Parser()
    except Exception as e:
        print "%s: error: %s" % (os.path.basename(sys.argv[0]), e)
        sys.exit(1)

    p.set_description("Search content files for a given search term.")
    p.set_epilog("Further information and usage examples can be found " \
                 "inside the documentation file for this script.")

    # Define required arguments
    p.add_avalue("-s", "--search-term", "term to search for", "search_term",
                 None, True)
    p.add_avalue("-d", "--directory", "directory containing the content " \
                 "files", "directory", None, True)

    # Define optional arguments
    p.add_switch("-c", "--case-sensitive", "do not ignore the case of the " \
                 "given search term", "case", False, False)
    p.add_switch("-h", "--help", "print this help message and exit", None,
                 True, False)
    p.add_switch(None, "--regex", "use regex syntax for the search term " \
                 "instead of just asterisk wildcards and semicolon " \
                 "separators (for details see the section \"Regular " \
                 "expression operations\" inside the Python documentation)",
                 "regex", True, False)
    p.add_switch(None, "--version", "print the version number and exit", None,
                 True, False)

    if len(sys.argv) == 1:
        p.error("At least one required argument is missing.")
    elif ("-h" in sys.argv) or ("--help" in sys.argv):
        p.print_help()
        sys.exit(0)
    elif "--version" in sys.argv:
        print finder.get_version()
        sys.exit(0)

    args = p.parse_args()
    try:
        print
        print "Searching for the given term. Please wait."

        match_count = 0
        match_files = 0

        content_files = finder.get_files(args.directory)
        for content_file in content_files:
            list_matches = finder.find_term(content_file, args.search_term,
                                            args.case, args.regex)

            if len(list_matches) > 0:
                match_count += len(list_matches)
                match_files += 1
                print
                print "  [%s]" % content_file.replace(args.directory, "")
                for match in list_matches:
                    print "    - %s" % match
                print

        total_files = len(content_files)
        just = common.get_max_digits([total_files, match_files, match_count])

        print "Search process completed."
        print
        print "Total files processed:   %s" % \
              str(total_files).rjust(just, " ")
        print
        if match_count == 0:
            print "No matches found."
        else:
            print "Total files matched:     %s" % \
                  str(match_files).rjust(just, " ")
            print "Total matches found:     %s" % \
                  str(match_count).rjust(just, " ")
        print
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF


#! /usr/bin/env python3

import argparse

from pydwf.dwf_function_signatures import dwf_function_signatures

def read_documentation_functions(filename):
    documented_functions = {}
    with open(filename, "r") as fi:
        section = None
        for line in fi:
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                continue
            if line.startswith("*"):
                section = line[1:].strip()
                continue

            documented_functions[line] = section
    return documented_functions

def report_headerfile_documentation_mismatches(filename):

    # First, get the header file functionm signatures.

    class typespec_null:
        def __getattr__(self, name):
            return None

    typespec = typespec_null()

    function_signatures = dwf_function_signatures(typespec)

    documented_functions = read_documentation_functions(filename)

    function_signature_names = {name: obsolete_flag for (name, rettype, params, obsolete_flag) in function_signatures}

    for (name, obsolete_flag) in function_signature_names.items():
        if name not in documented_functions:
            if obsolete_flag:
                obsolete = " (OBSOLETE)"
            else:
                obsolete = ""
            print("Header/Documentation mismatch: in header file but not in reference manual: {}{}".format(name, obsolete))

    for name in documented_functions:
        if name not in function_signature_names:
            print("Header/Documentation mismatch: in reference manual but not in header file: {} ({})".format(name, documented_functions[name]))

    print()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()

    report_headerfile_documentation_mismatches(args.filename)

if __name__ == "__main__":
    main()

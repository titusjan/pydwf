#! /usr/bin/env python3

import os
import subprocess
import base64
import contextlib
import tempfile
import shutil
import textwrap

def chop(s, n):
    """Chops 's' in pieces of length 'n'. The last part may be shorter than 'n'."""
    i = 0
    result = []
    while i < len(s):
        result.append(s[i:i+n])
        i += n
    return result

def zip_directory_to_blob(srcdir, name):
    """Copy a directory, zip it, and return the zip-file as a binary blob.
    """
    srcdir = os.path.abspath(srcdir)
    with tempfile.TemporaryDirectory() as tmpdir:
        original_working_directory = os.getcwd()
        os.chdir(tmpdir)
        try:
            shutil.copytree(srcdir, name)
            zipfile = name + ".zip"
            command_args = ["zip", "-o", "-r9", zipfile, name]
            subprocess.run(command_args, capture_output=True)
            with open(zipfile, "rb") as fi:
                data = fi.read()
            shutil.rmtree(name)
        finally:
            os.chdir(original_working_directory)
    return data

def print_zipped_directory_data(target_specifications, lhs_name):
        print("{} = {{".format(lhs_name))
        for (target_index, (target_name, target_directory)) in enumerate(target_specifications.items(), 1):
            target_data = zip_directory_to_blob(target_directory, target_name)
            print("    '{}':".format(target_name))
            comma = "" if target_index == len(target_specifications) else ","
            print("\n".join("        \"{}\"".format(line) for line in chop(base64.b64encode(target_data).decode("ascii"), 80)) + comma)
        print("}")

def main():

    target_specifications = {
        "pydwf-examples"  : "../../examples",
        "pydwf-html-docs" : "../../documentation/build/html"
    }

    filename = "../../pydwf/auxiliary_package_data.py"

    with open(filename, "w") as fo, contextlib.redirect_stdout(fo):

        comment ="""
            # The dictionary below contains zipped, base64-encoded directories that can be unpacked
            # using the "extract" commands of the pydwf main script ("python3 -m pydwf").
            #
            # They were generated by the 'maintainer/tools/make_auxiliary_package_data.py' script during the
            # deployment process.
            #
            # This is a workaround for the fact that there is currently no standardized way to have documentation
            # and examples in Python as part of the package. A Python package is just Python code, and that's it.
            #
            # Often, project deal with this by pointing to external websites for documentation (such as
            # readthedocs.io) and to another place (e.g. github, gitlab) where example scripts can be downloaded.
            #
            # I (SC) do not think this is right. The package code, its documentation, and its examples should
            # be distributed together, as one coherent entity. Therefore, we provide commands for the user to
            # extract examples and documentation at a location of their choice.
            #
            # To extract pydwf example scripts:
            #
            #     python -m pydwf extract-examples
            #
            # To extract the pydwf HTML documentation:
            #
            #     python -m pydwf extract-html docs
            #
            # The data that allows these commands to work is defined below.
        """

        print(textwrap.dedent(comment))
        print_zipped_directory_data(target_specifications, "targets")

if __name__ == "__main__":
    main()

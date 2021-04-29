#! /usr/bin/env python3

import os
import subprocess
import base64
import contextlib
import tempfile
import shutil
import hashlib
import time
import io

def chop(s, n):
    """Chops 's' in pieces of length 'n'. The last part may be shorter than 'n'."""
    i = 0
    result = []
    while i < len(s):
        result.append(s[i:i+n])
        i += n
    return result

print()

def random_filename(prefix, suffix):
    pass

#def directory_to_string(tmpdir, srcpath, name):

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

def make_zipped_directory_data(target_specifications):
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print("_zipped_directory_data = {")
        for (target_index, (target_name, target_directory)) in enumerate(target_specifications.items(), 1):
            target_data = zip_directory_to_blob(target_directory, target_name)
            print("    '{}':".format(target_name))
            comma = "" if target_index == len(target_specifications) else ","
            print("\n".join("        \"{}\"".format(line) for line in chop(base64.b64encode(target_data).decode("ascii"), 80)) + comma)
        print("}")
        #print()
        #print("    ZipFile(BytesIO(b64decode(targets[target]))).extractall()")
        #print()
    return f.getvalue()

def patch_python_script(scriptname, zipped_directory_data):
    fragments = []
    mode = 0 # 0: not yet found; 1: found, looking for closing '}'; 2: done.
    with open(scriptname, "r") as fi:
        for line in fi:
            if mode == 0:
                if "_zipped_directory_data = {" in line:
                    fragments.append(zipped_directory_data)
                    mode = 1
                else:
                    fragments.append(line)
            elif mode == 1:
                if "}" in line:
                    mode = 2
            else:
                fragments.append(line)

    with open(scriptname, "w") as fo:
        fo.write("".join(fragments))

def main():

    target_specifications = {
        "pydwf-examples"  : "../../examples",
        "pydwf-html-docs" : "../../doc/build/html"
    }

    zipped_directory_data = make_zipped_directory_data(target_specifications)

    patch_python_script("../../pydwf/__main__.py", zipped_directory_data)

if __name__ == "__main__":
    main()

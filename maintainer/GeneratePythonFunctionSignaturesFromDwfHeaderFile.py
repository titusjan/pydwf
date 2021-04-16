#! /usr/bin/env python3

import argparse
import re
from hashlib import md5
from contextlib import redirect_stdout

class TypeSpec:
    """Represents a C type."""
    def __init__(self, basetype, ptrflag, arraysize):

        assert (ptrflag is False) or (arraysize is None)

        self.basetype = basetype
        self.ptrflag  = ptrflag
        self.arraysize = arraysize

    def __repr__(self):
        return f"TypeSpec(basetype={self.basetype!r}, ptrflag={self.ptrflag!r}, arraysize={self.arraysize!r})"

    def emit(self):

        basetype = self.basetype.replace(' ', '_')
        if basetype[0].islower():
            basetype = "c_" + basetype

        if self.ptrflag:
            fulltype = f"{basetype}_ptr"
        elif self.arraysize is not None:
            fulltype = f"{basetype}_array_{self.arraysize}"
        else:
            fulltype = basetype

        return f"typespec.{fulltype}"

class ParSpec:
    """Represents a parameter."""
    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

    def __repr__(self):
        return f"ParSpec(name={self.name!r}, type_={self.type_!r})"

    def emit(self):
        return f"({self.name!r}, {self.type_.emit()})"

class FuncSpec:
    def __init__(self, name, returntype, parspecs, obsolete_flag):
        self.name = name
        self.returntype = returntype
        self.parspecs = parspecs
        self.obsolete_flag = obsolete_flag

    def __repr__(self):
        return f"FuncSpec(name={self.name!r}, returntype={self.returntype!r}, parspecs={self.parspecs!r}, obsolete_flag={self.obsolete_flag!r})"

    def emit(self):
        return f"({self.name!r}, {self.returntype.emit()}, [ {', '.join(parspec.emit() for parspec in self.parspecs)} ], {self.obsolete_flag!r})"

_partypes = [
    "void",
    "unsigned char", "unsigned short", "unsigned int", "unsigned long long",
    "bool",
    "char", "short", "int",
    "double",
    "HDWF",
    "FUNC", "ANALOGIO", "ENUMFILTER", "DEVID", "DEVVER", "DWFERC", "TRIGSRC", "TRIGLEN", "FILTER", "TRIGTYPE", "ACQMODE",
    "DwfState",
    "DwfParam",
    "DwfAnalogOutMode", "DwfAnalogOutIdle", "AnalogOutNode",
    "DwfDigitalInClockSource", "DwfDigitalInSampleMode",
    "DwfEnumConfigInfo",
    "DwfDigitalOutOutput", "DwfDigitalOutIdle", "DwfDigitalOutType",
    "DwfAnalogImpedance",
    "DwfTriggerSlope"
]

parspec_pattern =  f"({'|'.join(_partypes)}) (\\*)?([A-Za-z][A-Za-z0-9]*)(\\[(16|32|512)\\])?$"
re_parspec = re.compile(parspec_pattern)

def parse_parspec(s: str) -> ParSpec:
    m = re_parspec.match(s)
    assert m is not None
    basetype = m.group(1)
    ptrflag = (m.group(2) is not None)
    name = m.group(3)
    arraysize = int(m.group(5)) if m.group(5) is not None else None
    type_ = TypeSpec(basetype, ptrflag, arraysize)
    return ParSpec(name, type_)

def parse_funcspec(s: str, obsolete_flag: bool) -> FuncSpec:

    # part1 is the function prototype; part 2 are comments.
    part1, part2 = s.split(";", 1)

    idx = part1.find("(")
    part1a = part1[:idx]  # DWFAPI <returntype> <funcname>
    part1b = part1[idx:]  # ( parspec, parspec, ...)

    part1a = part1a.split()
    assert len(part1a) == 3
    (dwfapi, returntype, funcname) = part1a

    returntype = TypeSpec(returntype, False, None)

    assert part1b.startswith('(')
    assert part1b.endswith(')')

    part1b = part1b[1:-1]  # Get rid of the parentheses.

    parspecs = part1b.split(",")
    parspecs = [parspec.strip() for parspec in parspecs]
    parspecs = [parspec.strip() for parspec in parspecs if len(parspec) > 0]

    parspecs = [parse_parspec(parspec) for parspec in parspecs]
    header_func = funcname

    return FuncSpec(funcname, returntype, parspecs, obsolete_flag)

def parse_dwf_header_file(dwf_header_file):

    funcspecs = []
    obsolete_flag = False  # At the end of the header file, there are some functions that are declared 'obsolete'.

    for line in dwf_header_file.split("\n"):
        if "OBSOLETE" in line:
            obsolete_flag = True
        if line.startswith("DWFAPI"):
            funcspec = parse_funcspec(line, obsolete_flag)
            funcspecs.append(funcspec)

    return funcspecs

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--version", default=None)
    parser.add_argument("filename")

    args = parser.parse_args()

    if args.version is None:
        print("WARNING: no version specified. Use of the --version argument to specify a version of the DWF header file is recommended.")
        args.version ="(not specified)"

    with open(args.filename, "rb") as fi:
        dwf_header_file_binary_contents = fi.read()

    script_name = "GeneratePythonFunctionSignaturesFromDwfHeaderFile.py"

    dwf_header_file = dwf_header_file_binary_contents.decode("ascii")

    funcspecs = parse_dwf_header_file(dwf_header_file)

    output_filename = "dwf_function_signatures.py"

    with open(output_filename, "w") as fo:
        with redirect_stdout(fo):
            print("# *** This code was generated by the '{}' script, do not edit by hand! ***".format(script_name))
            print("#")
            print("# Generated from the Digilent Waveforms C header file:")
            print("#")
            print("#     file ......... :", args.filename)
            print("#     size ......... :", len(dwf_header_file_binary_contents), "bytes")
            print("#     md5sum ....... :", md5(dwf_header_file_binary_contents).hexdigest())
            print("#     version ...... :", args.version)
            print()
            print("from typing import List, Tuple, Any")
            print()
            print("def dwf_function_signatures(typespec: Any) -> List[Tuple[str, Any, List[Tuple[str, Any]], bool]]:")
            print()
            print("    \"\"\"Returns type information for the {} functions in the DWF API.\"\"\"".format(len(funcspecs)))
            print()
            print("    return [")
            print( ",\n".join("        " + funcspec.emit() for funcspec in funcspecs))
            print("    ]")

    print("Wrote Python file '{}'.".format(output_filename))

if __name__ == "__main__":
    main()

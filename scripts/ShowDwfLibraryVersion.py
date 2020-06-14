#! /usr/bin/env python3

from pydwf import DigilentWaveformLibrary

dwf = DigilentWaveformLibrary()

print("DWF library version: {!r}".format(dwf.getVersion()))

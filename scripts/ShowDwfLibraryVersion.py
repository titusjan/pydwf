#! /usr/bin/env python3

from pydwf import DigilentWaveformsLibrary

dwf = DigilentWaveformsLibrary()

print("DWF library version: {!r}".format(dwf.getVersion()))

#! /usr/bin/env python3

from pydwf import DigilentWaveformLibrary

def TestDigitalIO(device):
    # Version 3.12.1 of the DWF library has 19 'FDwfDigitalIO' functions, none of which are obsolete.
    # There are 3 generic functions (reset, configure, and status), and 8 functions that come in 32- and 64-bits variants.

    device.autoConfigureSet(False)

    digitalIO = device.digitalIO

    digitalIO.reset()

    # These are the two set functions.
    digitalIO.outputEnableSet(0x00005555)
    digitalIO.outputSet(0x0000aa55)
    digitalIO.configure()

    outputEnableInfo   = digitalIO.outputEnableInfo()
    outputEnableInfo64 = digitalIO.outputEnableInfo64()

    outputEnableGet   = digitalIO.outputEnableGet()
    outputEnableGet64 = digitalIO.outputEnableGet64()

    outputInfo   = digitalIO.outputInfo()
    outputInfo64 = digitalIO.outputInfo64()

    outputGet   = digitalIO.outputGet()
    outputGet64 = digitalIO.outputGet64()

    inputInfo   = digitalIO.inputInfo()
    inputInfo64 = digitalIO.inputInfo64()

    inputStatus   = digitalIO.inputStatus()
    inputStatus64 = digitalIO.inputStatus64()

    print("outputEnableInfo ...... : 0x{:08x}  0x{:016x}".format(outputEnableInfo, outputEnableInfo64))
    print("outputEnableGet ....... : 0x{:08x}  0x{:016x}".format(outputEnableGet, outputEnableGet64))
    print("outputInfo ............ : 0x{:08x}  0x{:016x}".format(outputInfo, outputInfo64))
    print("outputGet ............. : 0x{:08x}  0x{:016x}".format(outputGet, outputGet64))
    print("inputInfo ............. : 0x{:08x}  0x{:016x}".format(inputInfo, inputInfo64))
    print("inputStatus ........... : 0x{:08x}  0x{:016x}".format(inputStatus, inputStatus64))

def main():
    dwf = DigilentWaveformLibrary()
    serial_number = '210321AA214B'
    device = dwf.device.openBySerialNumber(serial_number)
    try:
        TestDigitalIO(device)
    finally:
        device.close()

if __name__ == "__main__":
    main()

#! /usr/bin/env python3

import time
import argparse
import contextlib

from pydwf import DigilentWaveformLibrary

def demonstrate_usage(serial_number: str) -> None:

    # The Digital I2C protocol interface has 11 methods:
    #
    # reset()
    # clear()
    #
    # stretchSet()
    # rateSet()
    # readNakSet()
    #
    # sclSet()
    # sdaSet()
    #
    # writeRead()
    # read()
    # write()
    # writeOne()

    dwf = DigilentWaveformLibrary()

    with contextlib.closing(dwf.device.openBySerialNumber(serial_number)) as device:

        i2c = device.digitalI2c

        i2c.reset()

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the I2C protocol functionality.")
    parser.add_argument('serial_number', help="serial number of the Digilent device")

    args = parser.parse_args()

    demonstrate_usage(args.serial_number)

if __name__ == "__main__":
    main()




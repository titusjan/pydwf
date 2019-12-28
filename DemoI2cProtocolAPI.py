#! /usr/bin/env python3

import time
import argparse
import contextlib

from pydwf import DigilentWaveformLibrary

def demo_i2c_protocol_api(i2c) -> None:

    # The Digital I2C protocol API has 11 methods:
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

    i2c.reset()


def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the I2C protocol API.")
    parser.add_argument('serial_number', help="serial number of the Digilent device")

    args = parser.parse_args()

    dwf = DigilentWaveformLibrary()
    with contextlib.closing(dwf.device.openBySerialNumber(args.serial_number)) as device:
        demo_i2c_protocol_api(device.digitalI2c)

if __name__ == "__main__":
    main()

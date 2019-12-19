#! /usr/bin/env python3

import time
import argparse
import contextlib

from pydwf import DigilentWaveformLibrary

def demonstrate_usage(serial_number: str) -> None:

    # The Digital SPI protocol interface has 18 methods:
    #
    # reset()
    #
    # frequencySet(hz: float)
    # clockSet(channel_index: int)
    # dataSet()
    # modeSet(mode: int)
    # orderSet(order: int)
    #
    # select(channel_index: int, level: int)
    #
    # writeRead()
    # writeRead16()
    # writeRead32()
    #
    # read()
    # readOne()
    # read16()
    # read32()
    #
    # write()
    # writeOne()
    # write16()
    # write32()

    dwf = DigilentWaveformLibrary()

    with contextlib.closing(dwf.device.openBySerialNumber(serial_number)) as device:

        spi = device.digitalSpi

        spi.reset()

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the SPI protocol functionality.")
    parser.add_argument('serial_number', help="serial number of the Digilent device")

    args = parser.parse_args()

    demonstrate_usage(args.serial_number)

if __name__ == "__main__":
    main()

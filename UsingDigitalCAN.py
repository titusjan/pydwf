#! /usr/bin/env python3

import time
import argparse
import contextlib

from pydwf import DigilentWaveformLibrary

def demonstrate_usage(serial_number: str) -> None:

    # The Digital CAN protocol interface has 7 methods:
    #
    # reset()
    #
    # rateSet(rate_hz: float)
    # polaritySet(high: int)
    #
    # txSet(channel_index: int)
    # rxSet(channel_index: int)
    #
    # tx()
    # rx()

    dwf = DigilentWaveformLibrary()

    with contextlib.closing(dwf.device.openBySerialNumber(serial_number)) as device:

        can = device.digitalCan

        can.reset()

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the CAN protocol functionality.")
    parser.add_argument('serial_number', help="serial number of the Digilent device")

    args = parser.parse_args()

    demonstrate_usage(args.serial_number)

if __name__ == "__main__":
    main()

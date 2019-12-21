#! /usr/bin/env python3

import argparse
import contextlib

from pydwf import DigilentWaveformLibrary

def demonstrate_usage(can) -> None:

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

    can.reset()

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the CAN protocol API.")
    parser.add_argument('serial_number', help="serial number of the Digilent device")

    args = parser.parse_args()

    dwf = DigilentWaveformLibrary()
    with contextlib.closing(dwf.device.openBySerialNumber(args.serial_number)) as device:
        demo_spi_protocol_api(device.digitalCan)

if __name__ == "__main__":
    main()

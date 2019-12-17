#! /usr/bin/env python3

import time
import argparse
import contextlib

from pydwf import DigilentWaveformLibrary

def demonstrate_usage(serial_number):
    # Version 3.12.1 of the DWF library has 19 'FDwfDigitalIO' functions, none of which are obsolete.
    # There are 3 generic functions (reset, configure, and status), and 8 functions that come in 32- and 64-bits variants.

    dwf = DigilentWaveformLibrary()

    with contextlib.closing(dwf.device.openBySerialNumber(serial_number)) as device:

        uart = device.digitalUart

        uart.reset()

        uart.rateSet(115200.0)
        uart.bitsSet(8)
        uart.paritySet(0)
        uart.stopSet(1)
        uart.txSet(0) # Loopback TX to RX, both on digital pin #0.
        uart.rxSet(0)

        i = 0
        (rx_buffer, parity_status) = uart.rx(0)  # Initialize reception
        while True:
            uart.tx("transmit {}\r\n".format(i).encode())
            (rx_buffer, parity_status) = uart.rx(100)
            print("Received:", (rx_buffer, parity_status))
            time.sleep(0.100)
            i += 1

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the DigitalUart protocol analyser.")
    parser.add_argument('serial_number', help="serial number of the Digilent device")

    args = parser.parse_args()

    demonstrate_usage(args.serial_number)

if __name__ == "__main__":
    main()

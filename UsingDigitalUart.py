#! /usr/bin/env python3

import time
import argparse
import contextlib

from pydwf import DigilentWaveformLibrary

def demonstrate_usage(serial_number):

    # The Digital UART protocol interface has 9 methods:
    # - reset()                                      -- reset the UART protocol functionality
    # - rateSet(), bitsSet(), paritySet(), stopSet() -- set UART protocol parameters
    # - txSet(), rxSet()                             -- select digital pins for transmit (TX) and receive (RX) directions.
    # - tx()                                         -- transmit data from the Digilent device;
    # - rx()                                         -- receive data into the Digilent device, -or-, initialize receiver if called with zero argument.

    dwf = DigilentWaveformLibrary()

    with contextlib.closing(dwf.device.openBySerialNumber(serial_number)) as device:

        uart = device.digitalUart

        uart.reset()

        # Setup UART communication for 115k2 baud, 8N1

        uart.rateSet(115200.0)
        uart.bitsSet(8)
        uart.paritySet(0)
        uart.stopSet(1)

        # Loopback TX to RX, both on digital I/O pin #0.

        uart.txSet(0)
        uart.rxSet(0)

        # Before starting to receive, we must initialize reception by calling the rx() method with size 0.
        uart.rx(0)

        # Repeatedly send and receive messages.
        i = 0
        while True:
            uart.tx("message #{}\r\n".format(i).encode())
            (rx_buffer, parity_status) = uart.rx(100)
            print("Received:", (rx_buffer, parity_status))
            time.sleep(0.100)
            i += 1

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the UART protocol analysis functionality.")
    parser.add_argument('serial_number', help="serial number of the Digilent device")

    args = parser.parse_args()

    demonstrate_usage(args.serial_number)

if __name__ == "__main__":
    main()

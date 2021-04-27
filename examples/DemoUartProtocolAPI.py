#! /usr/bin/env python3

import time
import argparse

from pydwf import DigilentWaveformsLibrary
from demo_utilities import find_demo_device, DemoDeviceNotFoundError

def demo_uart_protocol_api(uart):
    """Demonstrate the UART protocol functionality.

    The Digital UART protocol API has 9 methods, all of which are used in this demo.

    - reset()                                      -- reset the UART protocol functionality.
    - rateSet(), bitsSet(), paritySet(), stopSet() -- set UART protocol parameters.
    - txSet(), rxSet()                             -- select digital pins for transmit (TX) and receive (RX) directions.
    - tx()                                         -- transmit data from the Digilent device.
    - rx()                                         -- receive data into the Digilent device, -or-, initialize receiver if called with zero argument.
    """

    uart.reset()

    # Setup UART communication for 115k2 baud, 8N1.
    uart.rateSet(115200.0)
    uart.bitsSet(8)
    uart.paritySet(0)
    uart.stopSet(1)

    # Loopback TX to RX, both on digital I/O pin #0 -- no need to connect a physical loopback wire.
    uart.txSet(0)
    uart.rxSet(0)

    # Before starting to receive, we must initialize reception by calling the rx() method with size 0.
    uart.rx(0)

    # Loop until interrupted: repeatedly send and receive messages.
    i = 0
    while True:
        message = "UART message #{}".format(i).encode()
        uart.tx(message)
        (rx_buffer, parity_status) = uart.rx(100)
        print("Received message {} with parity status {}".format(rx_buffer, parity_status))
        time.sleep(0.100)
        i += 1

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the UART protocol API.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    args = parser.parse_args()

    try:
        dwf = DigilentWaveformsLibrary()
        with find_demo_device(dwf, args.serial_number) as device:
            demo_uart_protocol_api(device.digitalUart)
    except DemoDeviceNotFoundError:
        print("Could not find demo device, exiting.")
    except KeyboardInterrupt:
        print("Keyboard interrupt, ending demo.")

if __name__ == "__main__":
    main()

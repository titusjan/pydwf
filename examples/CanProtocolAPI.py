#! /usr/bin/env python3

import time
import argparse

from pydwf import DigilentWaveformsLibrary
from demo_utilities import find_demo_device, DemoDeviceNotFoundError

def demo_can_protocol_api(can) -> None:
    """Demonstrate the CAN protocol functionality.

    The Digital CAN protocol API has the following 7 methods.
    All of them are used below.

    - reset()                  -- reset the CAN protocol functionality.
    - rateSet(), polaritySet() -- set CAN protocol parameters.
    - txSet(), rxSet()         -- select digital pins for transmit (TX) and receive (RX) directions.
    - tx()                     -- transmit data from the Digilent device.
    - rx()                     -- receive data into the Digilent device, -or-, initialize receiver if called with zero argument.
    """

    can.reset()

    # Setup CAN communication for 125 kbits/sec.
    can.rateSet(125000.0)
    can.polaritySet(0)

    # Loopback TX to RX, both on digital I/O pin #0 -- no need to connect a physical loopback wire.
    can.txSet(0)
    can.rxSet(0)

    # Before starting to transmit, we must initialize transmission by calling the tx() method with vID equal to -1.
    can.tx(-1, 0, 0, b"")

    # Before starting to receive, we must initialize reception by calling the rx() method with size 0.
    (vID, extended, remote, data, status) = can.rx(0)

    # Loop until interrupted: repeatedly send and receive messages.
    i = 0
    while True:
        message = "CAN_{:04x}".format(i % 0x10000).encode()
        can.tx(17, 0, 0, message)
        (vID, extended, remote, data, status) = can.rx(8)
        print("Received message {} ; vID = {}, extended = {}, remote = {}, status = {}".format(data, vID, extended, remote, status))
        time.sleep(0.100)
        i += 1

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the CAN protocol API.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    args = parser.parse_args()

    try:
        dwf = DigilentWaveformsLibrary()
        with find_demo_device(dwf, args.serial_number) as device:
            demo_can_protocol_api(device.digitalCan)
    except DemoDeviceNotFoundError:
        print("Could not find demo device, exiting.")
    except KeyboardInterrupt:
        print("Keyboard interrupt, ending demo.")

if __name__ == "__main__":
    main()

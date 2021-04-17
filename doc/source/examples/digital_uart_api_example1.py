#! /usr/bin/env python3

import time
from pydwf import DigilentWaveformLibrary

# Initialize a DigilentWaveformLibrary instance.

dwf = DigilentWaveformLibrary()

# Open first available device.

device = dwf.device.open(-1)
try:
    # Get a reference to the device.digitalUart instrument.

    uart = device.digitalUart

    # Reset the UART protocol instrument.

    uart.reset()

    # Set UART protocol parameters.

    uart.rateSet(9600.0)  # 9600 baud
    uart.bitsSet(8)       # 8 data bits
    uart.paritySet(0)     # no parity (0=no parity, 1=odd parity, 2=even parity)
    uart.stopSet(1.0)     # 1 stop bit

    # Assign the TX and RX pins.
    # If they are the same (as below), we create a loopback without the need for a physical wire.

    uart.txSet(0)         # Put TX signal on digital pin #0.
    uart.rxSet(0)         # Get RX signal from digital pin #0.

    # Initialize the receiver.

    uart.rx(0)

    # Send and receive 10 UART messages.
    for i in range(10):
        message = "message #{}".format(i + 1).encode()
        uart.tx(message)
        time.sleep(0.100)
        (r, p) = uart.rx(100)
        print(r, p)

finally:
    device.close()
